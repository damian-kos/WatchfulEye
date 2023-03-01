import dearpygui.dearpygui as dpg


def error_handler(name):
    with dpg.window(modal=True, label="error") as error:
        dpg.add_text(f"{name}")
        dpg.add_button(
            label="OK",
            user_data=(name),
            width=100,
            callback=lambda: dpg.delete_item(error),
        )
    return False
