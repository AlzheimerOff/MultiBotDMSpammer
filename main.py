import discord
from discord.ext import commands
import json
import asyncio
import logging
import random
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('SpamBot')

VERSION = "1.0.0"
CREATOR = "Alzheimer"

ASCII_ART = f"""
        █████╗ ██╗     ███████╗██╗  ██╗███████╗██╗███╗   ███╗███████╗██████╗ 
        ██╔══██╗██║     ╚══███╔╝██║  ██║██╔════╝██║████╗ ████║██╔════╝██╔══██╗
        ███████║██║       ███╔╝ ███████║█████╗  ██║██╔████╔██║█████╗  ██████╔╝
        ██╔══██║██║      ███╔╝  ██╔══██║██╔══╝  ██║██║╚██╔╝██║██╔══╝  ██╔══██╗
        ██║  ██║███████╗███████╗██║  ██║███████╗██║██║ ╚═╝ ██║███████╗██║  ██║
        ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝
                                         V {VERSION}
"""

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

def save_config(new_config):
    with open('config.json', 'w') as f:
        json.dump(new_config, f, indent=2)

async def send_logs(ctx, target, author, bot_count, total_messages):
    cfg = load_config()
    log_channel_id = cfg.get('settings', {}).get('log_channel_id', 0)
    if log_channel_id == 0:
        return

    log_channel = ctx.bot.get_channel(log_channel_id)
    if not log_channel:
        return

    embed = discord.Embed(title="Nouveau Spam", color=discord.Color.purple())
    embed.add_field(name="Cible",
                    value=f"<@{target}>" if isinstance(target, int) else (target.mention if hasattr(target, 'mention') else str(target)),
                    inline=True)
    embed.add_field(name="Auteur", value=author.mention, inline=True)
    embed.add_field(name="Détails",
                    value=f"{bot_count} bots • {total_messages} messages",
                    inline=False)
    from datetime import datetime
    embed.timestamp = datetime.now()
    try:
        await log_channel.send(embed=embed)
    except:
        pass

def load_wl():
    if not os.path.exists('wl.json'):
        return []
    with open('wl.json', 'r') as f:
        try:
            return json.load(f)
        except:
            return []

def save_wl(wl_list):
    with open('wl.json', 'w') as f:
        json.dump(wl_list, f)

config = load_config()
tokens = config.get('tokens', [])
settings = config.get('settings', {})
prefix = settings.get('prefix', "+")
ADMIN_ID = 1442289590743339099

if not tokens:
    logger.error("Ajoute des tokens dans config.json")
    exit()

proxies = config.get('proxies', [])
bots = []

class SpamBot(commands.Bot):

    def __init__(self, *args, **kwargs):
        self.is_primary = kwargs.pop('is_primary', False)
        super().__init__(*args, **kwargs, help_command=None)

    async def on_ready(self):
        PURPLE = "\033[95m"
        GREEN = "\033[92m"
        RESET = "\033[0m"
        print(f"{PURPLE}Bot {GREEN}{self.user}{PURPLE} est connecté {RESET}")

        permissions = 442432 
        oauth_link = f"https://discord.com/api/oauth2/authorize?client_id={self.user.id}&permissions={permissions}&scope=bot%20applications.commands"

        try:
            links = {}
            if os.path.exists('oauth_links.json'):
                with open('oauth_links.json', 'r') as f:
                    links = json.load(f)
            links[str(self.user)] = oauth_link
            with open('oauth_links.json', 'w') as f:
                json.dump(links, f, indent=2)
        except:
            pass

        try:
            await self.change_presence(activity=discord.Streaming(
                name="dev by alzheimer", url="https://www.twitch.tv/alzheimer"))
        except:
            pass

    async def on_message(self, message):
        if message.author.bot:
            return
        if self.is_primary:
            await self.process_commands(message)

async def spam_by_id_chaos(bot, member_id, amount, message):
    await asyncio.sleep(random.uniform(0.01, 1.5))

    try:
        user = bot.get_user(member_id) or await bot.fetch_user(member_id)
    except Exception:
        return

    sent_count = 0
    target_amount = amount + random.randint(-10, 10)
    if target_amount < 1: target_amount = amount

    while sent_count < target_amount:
        if member_id in load_wl():
            return

        try:
            if proxies:
                bot.http.proxy = random.choice(proxies)

            await asyncio.sleep(random.uniform(0.1, 0.8))

            content = f"{user.mention} {message}"
            await user.send(content)
            sent_count += 1

        except discord.Forbidden:
            break
        except discord.HTTPException as e:
            if e.status == 429:
                await asyncio.sleep(random.uniform(2.0, 5.0))
            else:
                break
        except Exception:
            break

async def start_bots():
    primary_token = tokens[0]
    primary_bot = SpamBot(command_prefix=prefix,
                         intents=discord.Intents.all(),
                         is_primary=True)

    ALLOWED_ADMINS = [1442289590743339099, 1278456170662363198]

    @primary_bot.command(name="help")
    async def help_command(ctx):
        cfg = load_config()
        allowed_id = cfg.get('settings', {}).get('allowed_channel_id', 0)
        
        if ctx.author.id not in ALLOWED_ADMINS:
            if allowed_id != 0 and ctx.channel.id != allowed_id:
                return
        
        prefix_val = cfg.get('settings', {}).get('prefix', '+')
        
        try:
            embed = discord.Embed(
                title="Menu de commandes",
                description=f"Liste des commandes disponibles avec le préfixe {prefix_val}",
                color=discord.Color.purple()
            )
            
            embed.add_field(
                name="Spam",
                value=f"`{prefix_val}spam @user/ID message`",
                inline=False
            )
            
            embed.add_field(
                name="Réaction",
                value=f"`{prefix_val}react [emoji]` (Répondre au message)",
                inline=False
            )
            
            if ctx.author.id in ALLOWED_ADMINS:
                embed.add_field(
                    name="Administration",
                    value=(
                        f"`{prefix_val}wl @user` • Ajouter à la Whitelist\n"
                        f"`{prefix_val}unwl @user` • Retirer de la Whitelist\n"
                        f"`{prefix_val}salon #salon` • Salon autorisé\n"
                        f"`{prefix_val}logs #salon` • Salon des logs"
                    ),
                    inline=False
                )
        
            embed.set_footer(text=f"Demandé par {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
            from datetime import datetime
            embed.timestamp = datetime.now()
            
            await ctx.send(embed=embed)
        except discord.Forbidden:
            help_text = f"**Menu de commandes ({prefix_val})**\n\n"
            help_text += f"Spam : `{prefix_val}spam @user/ID message`\n"
            
            if ctx.author.id in ALLOWED_ADMINS:
                help_text += "\nAdministration :\n"
                help_text += f"• `{prefix_val}wl @user` • Whitelist\n"
                help_text += f"• `{prefix_val}unwl @user` • Unwhitelist\n"
                help_text += f"• `{prefix_val}salon #salon` • Config salon\n"
                help_text += f"• `{prefix_val}logs #salon` • Config logs\n"
            
            await ctx.send(help_text)
        except Exception as e:
            print(f"Erreur help: {e}")

    @primary_bot.command()
    async def spam(ctx, user_input: str = None, *, message: str = None):
        if user_input is None or message is None:
            prefix_val = load_config().get('settings', {}).get('prefix', '+')
            return await ctx.send(f"Utilisation correcte : `{prefix_val}spam @user/ID message`")

        cfg = load_config()
        allowed_id = cfg.get('settings', {}).get('allowed_channel_id', 0)
        if allowed_id != 0 and ctx.channel.id != allowed_id:
            if ctx.author.id not in ALLOWED_ADMINS: return

        member_id = None
        if user_input.startswith('<@') and user_input.endswith('>'):
            member_id = int(user_input.replace('<@!', '').replace('<@', '').replace('>', ''))
        else:
            try: member_id = int(user_input)
            except: return

        if member_id in load_wl():
            await ctx.send("Cette personne est Wl")
            return

        amount_per_bot = 50
        
        for i, b in enumerate(bots):
            async def force_react_launch(bot_instance, chan_id, msg_id, delay):
                await asyncio.sleep(delay)
                try:
                    channel = bot_instance.get_channel(chan_id)
                    if not channel:
                        channel = await bot_instance.fetch_channel(chan_id)
                    msg = await channel.fetch_message(msg_id)
                    await msg.add_reaction("😎")
                except:
                    pass
            asyncio.create_task(force_react_launch(b, ctx.channel.id, ctx.message.id, i * 0.1))

        await send_logs(ctx, member_id, ctx.author, len(bots), len(bots) * amount_per_bot)
        for b in bots:
            asyncio.create_task(spam_by_id_chaos(b, member_id, amount_per_bot, message))

    @primary_bot.command()
    async def wl(ctx, user_input: str):
        if ctx.author.id not in ALLOWED_ADMINS: return
        member_id = None
        if user_input.startswith('<@') and user_input.endswith('>'):
            member_id = int(user_input.replace('<@!', '').replace('<@', '').replace('>', ''))
        else:
            try: member_id = int(user_input)
            except: return
        current_wl = load_wl()
        if member_id not in current_wl:
            current_wl.append(member_id)
            save_wl(current_wl)
            await ctx.send(f"L'utilisateur {member_id} a été ajouté a la wl.")
        else:
            await ctx.send("Cet utilisateur est déjà dans la wl.")

    @primary_bot.command()
    async def unwl(ctx, user_input: str):
        if ctx.author.id not in ALLOWED_ADMINS: return
        member_id = None
        if user_input.startswith('<@') and user_input.endswith('>'):
            member_id = int(user_input.replace('<@!', '').replace('<@', '').replace('>', ''))
        else:
            try: member_id = int(user_input)
            except: return
        current_wl = load_wl()
        if member_id in current_wl:
            current_wl.remove(member_id)
            save_wl(current_wl)
            await ctx.send(f"L'utilisateur {member_id} a été retiré de la wl.")
        else:
            await ctx.send("Cet utilisateur n'est pas dans la wl.")

    @primary_bot.command()
    async def salon(ctx, channel: discord.TextChannel = None):
        if ctx.author.id not in ALLOWED_ADMINS: return
        cfg = load_config()
        if channel is None:
            cfg['settings']['allowed_channel_id'] = 0
            save_config(cfg)
            await ctx.send("Les commandes sont désormais autorisées dans tous les salons.")
        else:
            cfg['settings']['allowed_channel_id'] = channel.id
            save_config(cfg)
            await ctx.send(f"Les commandes sont désormais autorisé seulement au salon {channel.mention}.")

    @primary_bot.command()
    async def logs(ctx, channel: discord.TextChannel = None):
        if ctx.author.id not in ALLOWED_ADMINS: return
        cfg = load_config()
        if channel is None:
            cfg['settings']['log_channel_id'] = 0
            save_config(cfg)
            await ctx.send("Les logs de spam sont désormais désactivés.")
        else:
            cfg['settings']['log_channel_id'] = channel.id
            save_config(cfg)
            await ctx.send(f"Les logs de spam seront envoyés dans {channel.mention}.")

    @primary_bot.command()
    async def react(ctx, emoji: str):
        if not ctx.message.reference:
            return await ctx.send("Répond au message que tu veux faire réagir.")
        
        target_msg_id = ctx.message.reference.message_id
        target_chan_id = ctx.channel.id
        
        for i, b in enumerate(bots):
            async def force_react(bot_instance, chan_id, msg_id, delay, emo):
                await asyncio.sleep(delay)
                try:
                    channel = bot_instance.get_channel(chan_id)
                    if not channel:
                        channel = await bot_instance.fetch_channel(chan_id)
                    msg = await channel.fetch_message(msg_id)
                    await msg.add_reaction(emo)
                except:
                    pass
            asyncio.create_task(force_react(b, target_chan_id, target_msg_id, i * 0.1, emoji))

    bots.append(primary_bot)
    asyncio.create_task(primary_bot.start(primary_token))

    for token in tokens[1:]:
        bot = SpamBot(command_prefix=prefix, intents=discord.Intents.all(), is_primary=False)
        bots.append(bot)
        asyncio.create_task(bot.start(token))

async def main():
    PURPLE = "\033[95m"
    RESET = "\033[0m"
    print(f"{PURPLE}{ASCII_ART}{RESET}")
    print(f"{PURPLE}Créateur : {CREATOR}{RESET}")
    print(f"{PURPLE}" + "-" * 30 + f"{RESET}")
    await start_bots()
    while True:
        await asyncio.sleep(10)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
