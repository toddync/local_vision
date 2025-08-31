import asyncio
import signal

from bot import bot, token
from app import app

async def main():
    app_task = asyncio.create_task(app.run_async())
    bot_task = asyncio.create_task(bot.start(token))

    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()

    def _signal_handler():
        stop_event.set()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, _signal_handler)

    stop_task = asyncio.create_task(stop_event.wait())

    _, pending = await asyncio.wait(
        [app_task, bot_task, stop_task],
        return_when=asyncio.FIRST_COMPLETED,
    )

    for task in pending:
        task.cancel()

    if app_task and not app_task.done():
        await app.shutdown()

    if not bot_task.done():
        await bot.close()

    await asyncio.gather(*pending, return_exceptions=True)


if __name__ == "__main__":
    asyncio.run(main())
