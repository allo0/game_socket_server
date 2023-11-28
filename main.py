from classes.server import Server
from configs import logConf
from configs.appConf import Settings

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    if Settings.ENABLE_LOGS:
        logConf.configure_logging()

    my_server = Server()
    my_server.start_server()
