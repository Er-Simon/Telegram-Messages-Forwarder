import consts
import logger_config

from functools import partial
from telethon import TelegramClient, events
from telethon import utils as telethon_utils


logger = logger_config.get_logger()


def create_client(phone_number, api_id, api_hash):
    session_file_path = consts.SESSION_FILE_PATH.format(phone_number)
        
    logger.debug("TelegramClient path: {}".format(session_file_path))
        
    client = TelegramClient(
        session_file_path,
        api_id,
        api_hash,
    ) 
    
    return client

async def is_authorized(client:TelegramClient, phone_number):
    is_authorized = await client.is_user_authorized()
        
    if not is_authorized:
        logger.warning(f"Unauthorized account: {phone_number}")
        
        while True:
            logger.info("Sending a message to your Telegram account...")
        
            await client.send_code_request(phone_number)
        
            auth_code = input("Insert the received code: ")
            
            try:
                await client.sign_in(phone_number, auth_code)
            except Exception as e:
                logger.error(f"The account cannot be authorized, error: {e}")
            else:
                is_authorized = await client.is_user_authorized()
            
                if is_authorized:
                    logger.info(f"Account authorized: {phone_number}")
                    break

    return is_authorized

async def acquire_targets(client: TelegramClient):
    dialogs = await client.get_dialogs()

    dialogs_data = {
        index: {
            'id': dialogs[index].entity.id,
            'title': dialogs[index].name,
        } for index in range(len(dialogs))
    }
    
    for index in dialogs_data:
        logger.info('index: {} - id: {:>14} title: {}'.format(
            str(index).ljust(len(str(max(dialogs_data)))), 
            dialogs_data[index]['id'], 
            dialogs_data[index]['title']
        ))
        
    destination_entity = None
    while True:
        index = input("Insert the index of the destination chat: ").replace(" ", "")
        
        if index.isdigit():
            index = int(index)
            destination_entity = dialogs_data.get(index, None)

            if destination_entity:
                break
            
        logger.warning("You entered an invalid index, please try again.")
    
    target_entities = {}
    while True:
        index = input("Insert the index of the target chat: ").replace(" ", "")
        
        if index.isdigit():
            index = int(index)
            target_entity = dialogs_data.get(index, None)

            if target_entity:
                target_entities[len(target_entities)] = target_entity
                
                choice = input("Do you want to add another target(Y/n)? ").replace(" ", "").lower()
                
                if choice == 'n':
                    break
                
                continue
            
        logger.warning("You entered an invalid index, please try again.")
        
    return destination_entity, target_entities

async def handler(update:events.NewMessage, client:TelegramClient, destination_id):
    message_id = telethon_utils.get_message_id(update.message)
    source = update.message.peer_id
            
    logger.info(f"New message with id: {message_id} received from chat '{source}'")
    
    try:
        message = await client.send_message(destination_id, update.message)
    except Exception as e:
        logger.error("The message cannot be sent, error: {}".format(e))
    else:
        logger.info(f"Sent message with id: {message.id} to the chat '{message.peer_id}'")

async def initialize_handler(client: TelegramClient, destination, targets):    
    logger.info('The intercepted messages will be sent to chat with id: {:>14} - title: "{}"'.format(
        destination["id"],
        destination["title"]
    ))
    
    destination_id = destination["id"]
    
    logger.info("The following entities will be intercepted:")
    for index in targets:
        logger.info('index: {} - id: {:>14} title: "{}"'.format(
            str(index).ljust(len(str(max(targets)))), 
            targets[index]['id'], 
            targets[index]['title']
        ))
        
    target_ids = [
        targets[key]["id"] for key in targets
    ]
    
    func = partial(handler, client=client, destination_id=destination_id)
    
    client.add_event_handler(
        func, 
        events.NewMessage(
            chats=target_ids,
            incoming=True
    ))
    
    logger.info("Handler activated, intercepting messages.")
    logger.info("Press CTRL + C to terminate the execution")
    
    await client.run_until_disconnected()    

def start(user_data):
    client = create_client(
        user_data["phone_number"],
        user_data["api_id"],
        user_data["api_hash"]
    )
    
    with client:
        try:
            client.loop.run_until_complete(
                initialize_handler(
                    client,
                    user_data["destination"], 
                    user_data["targets"]
            ))
        except KeyboardInterrupt:
            pass
        
    logger.info("Telegram client stopped and terminating correctly.")        

async def initialize(client: TelegramClient, phone_number):
    entities = None
    
    await client.connect()

    authorized = await is_authorized(client, phone_number)
    
    if authorized:
        destination, targets = await acquire_targets(client)
        entities = destination, targets
        
    await client.disconnect()
        
    return entities
        
def initialize_user_data():
    user_data = None
    
    logger.info("To retrieve your Telegram `api_id` and `api_hash` visit the https://my.telegram.org and log in with your Telegram account.")
    
    phone_number = input("Insert Telegram account phone number (with country prefix, e.g., +1 for USA): ").replace(" ", "")
    logger.info(f"User entered phone number: {phone_number}")

    api_id = input("Insert api_id: ").replace(" ", "")
    logger.info("User entered api_id: {}".format(api_id))

    api_hash = input("Insert api_hash: ").replace(" ", "")
    logger.info("User entered api_hash: {}".format(api_hash))
    
    client = None
    try:
        client = create_client(phone_number, api_id, api_hash)
    except Exception as e:
        logger.error('Cannot be created a Telegram Client, error: {}'.format(e))

    if client:
        try:
            destination, targets = client.loop.run_until_complete(initialize(client, phone_number))
        except Exception as e:
            logger.error('The account cannot be initialized, error: {}'.format(e))
        else:
            user_data = {
                'phone_number': phone_number,
                'api_id': api_id,
                'api_hash': api_hash,
                'destination': destination,
                'targets': targets
            }
        
    return user_data