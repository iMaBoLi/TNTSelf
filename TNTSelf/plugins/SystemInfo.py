from TNTSelf import client
import platform
from datetime import datetime
import psutil

@client.Command(command="Sysinfo")
async def systeminfo(event):
    await event.edit(client.STRINGS["wait"])
    uname = platform.uname()
    softw = "**• System Information:**\n"
    softw += f"    **- System:** ( `{uname.system}` )\n"
    softw += f"    **- Release:** ( `{uname.release}` )\n"
    softw += f"    **- Version:** ( `{uname.version}` )\n"
    softw += f"    **- Machine:** ( `{uname.machine}` )\n\n"
    bt = datetime.fromtimestamp(psutil.boot_time())
    softw += f"**• Boot Time:** ( `{bt.day}/{bt.month}/{bt.year}` - `{bt.hour}:{bt.minute}:{bt.second}` )\n\n"
    softw += "**• CPU Information:**\n"
    softw += f"    **- Physical Cores:** ( `{str(psutil.cpu_count(logical=False))}` )\n"
    softw += f"    **- Total Cores:** ( `{str(psutil.cpu_count(logical=True))}` )\n"
    softw += f"    **- Cores Usage:** ( `{psutil.cpu_percent()}%` )\n"
    svmem = psutil.virtual_memory()
    softw += "**• Memory Usage:**\n"
    softw += f"    **- Total:** ( `{client.functions.convert_bytes(svmem.total)}` )\n"
    softw += f"    **- Available:** ( `{client.functions.convert_bytes(svmem.available)}` )\n"
    softw += f"    **- Used:** ( `{client.functions.convert_bytes(svmem.used)}` )\n"
    softw += f"    **- Percentage:** ( `{svmem.percent}%` )"
    await event.edit(softw)