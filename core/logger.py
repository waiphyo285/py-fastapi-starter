import logging
import colorlog

# Configure the logger
def configure_logger():
    logger = logging.getLogger("Logger")
    logger.setLevel(logging.DEBUG)
    
    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    log_colors = {
        'DEBUG': 'bold_cyan',
        'INFO': 'bold_blue',
        'WARNING': 'yellow',
        'ERROR': 'bold_red',
        'CRITICAL': 'bold_red',
    }
    
    # Create a colorful formatter
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(levelname)-6s - %(name)s - %(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors=log_colors
    )
    
    # Set the formatter for the console handler
    console_handler.setFormatter(formatter)
    
    # Add the console handler to the logger
    logger.addHandler(console_handler)
    
    return logger

# Initialize logger
logger = configure_logger()
