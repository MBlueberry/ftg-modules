from telethon.utils import get_display_name, get_peer_id

from .. import loader, utils


@loader.tds
class MessageStillerMod(loader.Module):
    """ """
    strings = {'name': 'MessageStiller'}

    async def client_ready(self, client, db):
        self.db = db

    async def stillcmd(self, message):
        """ """
        ms = self.db.get("MessageStiller", "ms", {})
        args = utils.get_args(message)
        if not args:
            return await message.edit("<b>Нет аргументов после команды.</b>")

        try:
            from_chat = await message.client.get_entity(int(args[0]) if args[0].isnumeric() else args[0])
            to_chat = await message.client.get_entity(int(args[1]) if args[1].isnumeric() else args[1])
        except ValueError:
            return await message.edit("<b>Ошибка ввода аргументов.</b>")

        name1 = get_display_name(from_chat)
        name2 = get_display_name(to_chat)

        self.db.set("MessageStiller", "ms", {get_peer_id(from_chat): get_peer_id(to_chat)})
        await message.edit(f"<b>[MessageStiller]</b> С {name1} в {name2}.\nВключено!")
    
    async def msclearcmd(self, message):
        """ """
        self.db.set("MessageStiller", "ms", {})
        return await message.edit(f"<b>[MessageStiller]</b> Отключено!")


    async def watcher(self, message):
        """ """
        ms = self.db.get("MessageStiller", "ms")
        if message.chat_id in ms:
            msg = await message.client.get_messages(message.chat_id, ids=message.id)
            if msg and msg.text:
                await message.client.send_message(ms[message.chat_id], "/s " + msg.text)