from FidoSelf import client
from carbonnow import Carbon
import os

@client.Command(
    commands={
        "EN": "Carbon",
        "FA": "کربن",
    }
)
async def carbontext(event):
    code = event.reply_message.text
    carbon = Carbon(
        code=code, # Your Code
        background='#4a90e6',  # Optional: Hex-Color for Background
        drop_shadow=True,  # Optional: Drop Shadow on div Box
        drop_shadow_blur='68px',  # Optional: Drop Shadow Blur on div Box
        drop_shadow_offset='20px',  # Optional: Drop Shadow Offset on div Box
        export_size='4x',  # Optional: Export Size (1x, 2x, 4x)
        font_size='14px',  # Optional: Font size
        font_family='Fira Code',  # Optional: support FontFamily on carbon.now.sh
        first_line_number=1,  # Optional: Starting Line Numbers if Line Numbers Exist
        language='javascript',  # Optional: Programming Language of Choice
        line_height='133%',  # Optional: Line Height
        line_numbers=False,  # Optional: Line Numbers
        padding_horizontal='56px',  # Optional: Horizontal Padding
        padding_vertical='56px',  # Optional: Vertical Padding
        theme='Material',  # Optional: Carbon Theme
        watermark=False,  # Optional: Carbon Watermark
        width_adjustment=True,  # Optional: Width Adjustment
        window_controls=False,  # Optional: Window Controls
        window_theme='Material',  # Optional: Window Theme
    )
    await carbon.save("CarbonText")
    filename = "CarbonText.jpg"
    await event.respond(client.get_string("CarbonText_2"), file=filename)
    os.remove(filename)
    await event.delete()
