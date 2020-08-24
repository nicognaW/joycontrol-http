import asyncio
import logging
import multiprocessing as mp
import os
from argparse import Namespace
from time import sleep

import uvicorn
from uvicorn import Config

import http
from joycontrol import logging_default as log, utils
from joycontrol.controller import Controller
from joycontrol.memory import FlashMemory
from joycontrol.protocol import controller_protocol_factory
from joycontrol.server import create_hid_server

logger = logging.getLogger(__name__)

log.configure()


async def main(args, q):
    # parse the spi flash
    logger.name = "CLI进程"
    if args.spi_flash:
        with open(args.spi_flash, 'rb') as spi_flash_file:
            spi_flash = FlashMemory(spi_flash_file.read())
    else:
        # Create memory containing default controller stick calibration
        spi_flash = FlashMemory()

    # Get controller name to emulate from arguments
    controller = Controller.from_arg(args.controller)

    with utils.get_output(path=args.log, default=None) as capture_file:
        # prepare the the emulated controller
        factory = controller_protocol_factory(controller, spi_flash=spi_flash)
        ctl_psm, itr_psm = 17, 19
        transport, protocol = await create_hid_server(factory, reconnect_bt_addr=args.reconnect_bt_addr,
                                                      ctl_psm=ctl_psm,
                                                      itr_psm=itr_psm, capture_file=capture_file,
                                                      device_id=args.device_id)

        controller_state = protocol.get_controller_state()

        logger.debug("controller开始监听")
        while True:
            await asyncio.sleep(0.1)
            if q.empty():
                continue
            msg = q.get()
            print(str(msg))


def run_cli(q):
    args = Namespace()
    setattr(args, "controller", "PRO_CONTROLLER")
    setattr(args, "device_id", None)
    setattr(args, "log", "log.log")
    setattr(args, "nfc", None)
    setattr(args, "reconnect_bt_addr", None)
    setattr(args, "spi_flash", None)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        main(args, q)
    )


def run_server(q):
    server.run()


shouldStop = False


def run_main_loop(q):
    sub_q = mp.Queue()
    logger.name = "主循环进程"
    cli_p = mp.Process(args=(sub_q,), target=run_cli, name="cli")
    http.cli_p = cli_p
    cli_p.start()
    sub_q.put({"msg": "test"})
    while not shouldStop:
        try:
            empty = q.empty()
            sleep(0.1)
            # if not cli_p.is_alive():
            #     cli_p.start()
            if not empty:
                msg = q.get_nowait()
                print(f"收到消息：{msg['msg']}")
                if msg['msg'] == "restart":
                    logger.debug("重启cli进程...")
                    logger.debug("终止cli进程...")
                    cli_p.terminate()
                    cli_p.join()
                    logger.debug("关闭cli进程...")
                    cli_p.close()
                    logger.debug("删除cli进程...")
                    del cli_p
                    logger.debug("创建新的cli进程...")
                    cli_p = mp.Process(args=(http.q,), target=run_cli, name="cli")
                    if not cli_p.is_alive():
                        logger.debug("开启新的cli进程...")
                        cli_p.start()
        except Exception as e:
            print(e.__str__())


if __name__ == '__main__':

    if not os.geteuid() == 0:
        raise PermissionError('Script must be run as root!')

    server = uvicorn.Server(Config("http:app", host="0.0.0.0", port=80, reload=True))

    http.q = mp.Queue()
    http.isServerRunning = True

    main_loop_p = mp.Process(args=(http.q,), target=run_main_loop, name="loop")

    main_loop_p.start()

    run_server(http.q)
