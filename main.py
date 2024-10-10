import consts
import logger_config
import utils
import telegram_message_forwarder
    
logger = logger_config.get_logger()

if __name__ == '__main__':
    logger.info("Start execution")
    
    user_data = utils.loads_data()
    
    if not user_data:
        logger.warning("No user data loaded. Starting initialize user data process.")
        
        user_data = telegram_message_forwarder.initialize_user_data()
        
        if user_data:
            utils.dumps_data(user_data)            
            
            logger.info("User data saved successfully.")
    else:
        logger.info("User data loaded successfully.")
        
        logger.info("If you want to reset your settings, delete the file at the current path: {}".format(consts.CONFIG_FILE_PATH))
        
    if user_data:
        telegram_message_forwarder.start(user_data)
    
    logger.info("End of execution")
        
        