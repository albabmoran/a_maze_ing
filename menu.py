from mazedraw import ProgramState, MazeDrawer


class Menu:
    def __init__(self, state: ProgramState, visual: MazeDrawer) -> None:
        self.state: ProgramState = state
        self.visual: MazeDrawer = visual

    def key_press(self, key: int, visual: MazeDrawer) -> None:
        state = visual.state

        if key == ord('1'):
            state.regenerate()

        elif key == ord('2'):
            state.toggle_solution()

        elif key == ord('3'):
            state.rotate_palette()

        elif key == ord('4'):
            state.rotate_wall_color()

        elif key == ord('5'):
            state.toggle_animation()

        elif key == ord('6'):
            state.quit()
            visual.close()

        state.need_redraw = True
