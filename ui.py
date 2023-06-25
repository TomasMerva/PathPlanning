import pygame, pygame_gui


class UI:
    def __init__(self, width, height, gui_scale):
        self.WIDTH = width
        self.HEIGHT = height
        self.GUI_SCALE = gui_scale
        self.clock = pygame.time.Clock()
        self.manager = None
        self.toolbar_container, self.toolbar_ui = None, None

    def init_ui(self):
        self.manager = pygame_gui.UIManager((self.WIDTH, self.WIDTH), "theme.json")
        self.toolbar_container = pygame_gui.core.UIContainer(
            pygame.Rect(0, 0, int(self.GUI_SCALE*self.WIDTH), self.HEIGHT),
            manager=self.manager,
            starting_height=0 
            )
        self.toolbar_ui = pygame_gui.elements.UIPanel(
            pygame.Rect(0, 0, int(self.GUI_SCALE*self.WIDTH), self.HEIGHT),
            starting_height=1,
            manager=self.manager,
            container=self.toolbar_container,
            object_id='toolbar'
        )

        # Choosing environment
        self.environment_menu = {
            "label" : pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(0.025*self.WIDTH+30, 20, 100, 40),
                text='Environment:',  
                manager=self.manager,
                container=self.toolbar_ui,
                object_id='env_label'
            ),
            "dropdown_menu" : pygame_gui.elements.UIDropDownMenu(
                options_list=self.env_list, 
                starting_option=self.current_env_type,
                relative_rect=pygame.Rect((200, 20), (200, 40)), 
                manager=self.manager,
                container=self.toolbar_ui,
                expansion_height_limit=100
            )
        }

        """
        DISCRETE PLANNERS
        """
        # Planners
        self.planner_discrete_ui = pygame_gui.elements.UIPanel(
            pygame.Rect(0.025*self.WIDTH, 100, int((self.GUI_SCALE-0.05)*self.WIDTH), self.HEIGHT-150),
            starting_height=1,
            manager=self.manager,
            container=self.toolbar_container,
            object_id='planner_toolbar'
        )
        # Selecting discrete planners
        self.planner_discrete_menu = {
            "label" : pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(20, 20, 100, 50),
                text='Planner:',  
                manager=self.manager,
                container=self.planner_discrete_ui,
                object_id='plannel_label'
                ),
            "dropdown_menu" : pygame_gui.elements.UIDropDownMenu(
                options_list=self.planners_discrete_list, 
                starting_option=self.default_discrete_planner,
                relative_rect=pygame.Rect((140, 20), (250, 50)), 
                manager=self.manager,
                container=self.planner_discrete_ui,
                expansion_height_limit=100
                ),
            "reset_button" : pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((20, -75), (200, 50)), 
                text='Reset environment',
                manager=self.manager, 
                container=self.planner_discrete_ui,
                anchors={'left': 'left',
                         'bottom': 'bottom'}
                ),
            "solve_button" : pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((-220, -75), (200, 50)), 
                text='Solve',
                manager=self.manager, 
                container=self.planner_discrete_ui,
                anchors={'right': 'right',
                         'bottom': 'bottom'}
                )
        }

        """
        Continuous planners
        """
        self.planner_continuous_ui = pygame_gui.elements.UIPanel(
            pygame.Rect(0.025*self.WIDTH, 100, int((self.GUI_SCALE-0.05)*self.WIDTH), self.HEIGHT-150),
            starting_height=1,
            manager=self.manager,
            container=self.toolbar_container,
            object_id='planner_toolbar'
        )
        # Selecting discrete planners
        self.planner_continuous_menu = {
            "label" : pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(20, 20, 100, 50),
                text='Planner:',  
                manager=self.manager,
                container=self.planner_continuous_ui,
                object_id='plannel_label'
                ),
            "dropdown_menu" : pygame_gui.elements.UIDropDownMenu(
                options_list=self.planners_continuous_list, 
                starting_option=self.default_continuous_planner,
                relative_rect=pygame.Rect((140, 20), (250, 50)), 
                manager=self.manager,
                container=self.planner_continuous_ui,
                expansion_height_limit=100
                ),
            "reset_button" : pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((20, -75), (200, 50)), 
                text='Reset environment',
                manager=self.manager, 
                container=self.planner_continuous_ui,
                anchors={'left': 'left',
                         'bottom': 'bottom'}
                ),
            "solve_button" : pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((-220, -75), (200, 50)), 
                text='Solve',
                manager=self.manager, 
                container=self.planner_continuous_ui,
                anchors={'right': 'right',
                         'bottom': 'bottom'}
                )
        }
        self.planner_discrete_ui.show()
        self.planner_continuous_ui.hide()
