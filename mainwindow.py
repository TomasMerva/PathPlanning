import pygame, pygame_gui
from ui import UI
from colors import Colors
from discrete_world import DiscreteWorld

class MainWindow(UI):
    def __init__(self, width, height, gui_scale):
        super().__init__(width, height, gui_scale)
        # Physical properties
        self.WIDTH = width
        self.HEIGHT = height
        self.GUI_SCALE = gui_scale
        pygame.init()
        pygame.display.set_caption('Path planning algorithms')
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.colors_list = Colors()

        # --------
        # Planners
        # --------
        self.env_list = ["Discrete",
                         "Continuous"
                         ]
        self.current_env_type = self.env_list[0]
        # Discrete
        self.planners_discrete_list = ["Breadth First Search",
                                       "Depth First Search",
                                       "Djisktra Search",
                                       "A* Search"
                                      ]
        self.default_discrete_planner = "Breadth First Search"
        # Continuous
        self.planners_continuous_list = ["Potential Field"
                                        ]
        self.default_continuous_planner = "Potential Field"

        self.init_ui()

        # --------
        # Discrete env
        # --------
        self.discrete_env = DiscreteWorld(self.WIDTH, self.HEIGHT, self.GUI_SCALE, rows=10)
        self.discrete_env.make_grid()
        self.discrete_env.draw(self.window)


    def spin(self):
        time_delta = self.clock.tick(60)/1000.0
        # Check events
        for event in pygame.event.get():
            # Check if the close button was clicked
            if event.type == pygame.QUIT:
                return False
            
            if pygame.mouse.get_pressed()[0] and self.current_env_type == "Discrete":
                if not self.discrete_env.start_node:
                    self.discrete_env.start_node = self.discrete_env.get_mouse_clicked_node()
                    self.discrete_env.start_node.make_start()

                elif not self.discrete_env.goal_node and self.current_env_type == "Discrete":
                    temp_node = self.discrete_env.get_mouse_clicked_node()
                    if temp_node != self.discrete_env.start_node:
                        self.discrete_env.goal_node = temp_node
                        self.discrete_env.goal_node.make_goal()
                
            """
            UI buttons
            """
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                # Discrete environment
                if event.ui_element == self.planner_discrete_menu["reset_button"]:
                    print("Resetting discrete environment...")
                    self.discrete_env.start_node = None
                    self.discrete_env.goal_node = None
                    self.discrete_env.make_grid()
                elif event.ui_element == self.planner_discrete_menu["solve_button"]:
                    print("Solving discrete environment...")
                # Continuous environment
                elif event.ui_element == self.planner_continuous_menu["reset_button"]:
                    print("Resetting continuous environment...")
                elif event.ui_element == self.planner_continuous_menu["solve_button"]:
                    print("Solving continuous environment...")
                
            """
            UI dropdown menu
            """
            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                # Choosing environment
                if event.ui_element == self.environment_menu["dropdown_menu"]:
                    if event.text == "Discrete":
                        self.planner_discrete_ui.show()
                        self.planner_continuous_ui.hide()
                        self.current_env_type = "Discrete"
                        self.discrete_env = DiscreteWorld(self.WIDTH, self.HEIGHT, self.GUI_SCALE, rows=10)
                        self.discrete_env.make_grid()
                    elif event.text == "Continuous":
                        self.planner_continuous_ui.show()
                        self.planner_discrete_ui.hide()
                        self.current_env_type = "Continuous"
                    


            self.manager.process_events(event)

        if self.current_env_type == "Discrete":
            self.discrete_env.draw(self.window)

        self.manager.update(time_delta)
        self.manager.draw_ui(self.window)
        pygame.display.update()
        return True
    

    def draw(self):
        if self.current_env_type == "Discrete":
            self.window.fill(self.colors_list.WHITE)    # Reset pygame window
            self.discrete_env.draw()
        elif self.current_env_type == "Continuous":
            self.window.fill(self.colors_list.WHITE)    # Reset pygame window


if __name__=="__main__":
    mainwindow = MainWindow(1600, 800, 0.4)
    run = True
    while run:
        run = mainwindow.spin()