import discord
from discord.ext import commands
import os

# Bot Intents
intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.reactions = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Server and Role Info
GUILD_ID = 1352343367660343306  # Replace with your actual server ID
VERIFY_EMOJI = "🎟️"

@bot.event
async def on_ready():
    print(f'✅ Bot is online as {bot.user}!')

@bot.command()
@commands.has_permissions(administrator=True)
async def setup_server(ctx):
    guild = ctx.guild

    await ctx.send("🛠️ Starting server setup...")

    # Delete Categories & Channels
    for category in guild.categories:
        try:
            await category.delete()
        except Exception as e:
            print(f"⚠️ Failed to delete category {category.name}: {e}")

    for channel in guild.channels:
        try:
            await channel.delete()
        except Exception as e:
            print(f"⚠️ Failed to delete channel {channel.name}: {e}")

    # Create Roles
    verified_role = discord.utils.get(guild.roles, name="Verified")
    vip_role = discord.utils.get(guild.roles, name="VIP")
    staff_role = discord.utils.get(guild.roles, name="Staff")

    if not verified_role:
        verified_role = await guild.create_role(name="Verified")
    if not vip_role:
        vip_role = await guild.create_role(name="VIP")
    if not staff_role:
        staff_role = await guild.create_role(name="Staff")

    everyone_role = guild.default_role

    # Server Info Category
    info_cat = await guild.create_category("《👑》 Server Info")

    await info_cat.create_text_channel(
        "📝︱welcome",
        overwrites={everyone_role: discord.PermissionOverwrite(read_messages=True, send_messages=False)}
    )

    await info_cat.create_text_channel(
        "📜︱rules",
        overwrites={everyone_role: discord.PermissionOverwrite(read_messages=True, send_messages=False)}
    )

    verify_channel = await info_cat.create_text_channel(
        "✅︱verify-here",
        overwrites={everyone_role: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=True)}
    )

    # Send Verify Embed
    embed = discord.Embed(
        title="🎟️ Verify Here!",
        description=f"React with {VERIFY_EMOJI} to verify yourself and unlock the server!",
        color=discord.Color.green()
    )
    verify_message = await verify_channel.send(embed=embed)
    await verify_message.add_reaction(VERIFY_EMOJI)

    # General Chat Category
    general_cat = await guild.create_category(
        "《💭》 General Chat",
        overwrites={
            everyone_role: discord.PermissionOverwrite(read_messages=False),
            verified_role: discord.PermissionOverwrite(read_messages=True)
        }
    )

    await general_cat.create_text_channel("💬︱general-chat")
    await general_cat.create_text_channel("🎨︱media-showcase")
    await general_cat.create_text_channel("📈︱polls")
    await general_cat.create_text_channel("🎉︱giveaways")

    # Development Zone
    dev_cat = await guild.create_category(
        "《💻》 Development Zone",
        overwrites={
            everyone_role: discord.PermissionOverwrite(read_messages=False),
            verified_role: discord.PermissionOverwrite(read_messages=True)
        }
    )

    await dev_cat.create_text_channel("📂︱releases")
    await dev_cat.create_text_channel("⚙︱tools-database")
    await dev_cat.create_text_channel("🔬︱offsets-and-sigs")
    await dev_cat.create_text_channel("💻︱coding-help")
    await dev_cat.create_text_channel("📑︱tutorials")

    # VIP Section
    vip_cat = await guild.create_category(
        "《💎》 VIP Section",
        overwrites={
            everyone_role: discord.PermissionOverwrite(read_messages=False),
            vip_role: discord.PermissionOverwrite(read_messages=True)
        }
    )

    await vip_cat.create_text_channel("🔒︱vip-chat")
    await vip_cat.create_text_channel("🔒︱exclusive-dumps")
    await vip_cat.create_text_channel("🔒︱premium-scripts")

    # Staff HQ
    staff_cat = await guild.create_category(
        "《🛡️》 Staff HQ",
        overwrites={
            everyone_role: discord.PermissionOverwrite(read_messages=False),
            staff_role: discord.PermissionOverwrite(read_messages=True)
        }
    )

    await staff_cat.create_text_channel("🛡︱staff-chat")
    await staff_cat.create_text_channel("🔨︱ban-logs")
    await staff_cat.create_text_channel("📋︱user-reports")
    await staff_cat.create_text_channel("🖥︱staff-tools")

    await ctx.send("✅ Server setup complete! React in **verify-here** to unlock the server!")

@bot.event
async def on_raw_reaction_add(payload):
    if payload.member is None or payload.member.bot:
        return

    if str(payload.emoji) != VERIFY_EMOJI:
        return

    guild = bot.get_guild(GUILD_ID)
    if guild is None:
        return

    verified_role = discord.utils.get(guild.roles, name="Verified")
    if not verified_role:
        return

    member = guild.get_member(payload.user_id)
    if member is None:
        return

    if verified_role in member.roles:
        return

    await member.add_roles(verified_role)

    try:
        await member.send("✅ You are now verified and have access to the full server!")
    except discord.Forbidden:
        print(f"Couldn't DM {member.display_name}")

    print(f"✅ {member.display_name} has been verified!")

# Securely get token from environment variable or directly
TOKEN = os.environ.get('TOKEN')
if not TOKEN:
    TOKEN = 'MTM0ODA5ODIyMDk3NDQxMTgxNw.G-89Tr.VHR-hfFiILhwH34NzxWmnUkpe-mi8PtpynJ4Fc'  # Fallback, but not recommended!

bot.run(TOKEN)