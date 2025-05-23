from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import tcod.event

import actions
from actions import (
  Action, 
  BumpAction, 
  PickupAction, 
  WaitAction)

import color
import exceptions

if TYPE_CHECKING:
  from engine import Engine
  from entity import Item
  
MOVE_KEYS = {
  # (-1, -1) , (0, -1) , (1, -1)
  # (-1, 0)  , (0, 0)  , (1, 0)
  # (-1, 1)  , (1, 0)  , (1, 1)
  # arrow keys
  tcod.event.K_UP: (0, -1),
  tcod.event.K_DOWN: (0, 1),
  tcod.event.K_LEFT: (-1, 0),
  tcod.event.K_RIGHT: (1, 0),
  tcod.event.K_HOME: (-1, -1),
  tcod.event.K_END: (-1, 1),
  tcod.event.K_PAGEUP: (1, -1),
  tcod.event.K_PAGEDOWN: (1, 1),
  # numpad keys
  tcod.event.K_KP_1: (-1, 1),
  tcod.event.K_KP_2: (0, 1),
  tcod.event.K_KP_3: (1, 1),
  tcod.event.K_KP_4: (-1, 0),
  tcod.event.K_KP_6: (1, 0),
  tcod.event.K_KP_7: (-1, -1),
  tcod.event.K_KP_8: (0, -1),
  tcod.event.K_KP_9: (1, -1),
  # vi keys
  tcod.event.K_h: (-1, 0),
  tcod.event.K_j: (0, 1),
  tcod.event.K_k: (0, -1),
  tcod.event.K_l: (1, 0),
  tcod.event.K_y: (-1, -1),
  tcod.event.K_u: (1, -1),
  tcod.event.K_b: (-1, 1),
  tcod.event.K_n: (1, 1),
}

WAIT_KEYS = {
  tcod.event.K_PERIOD,
  tcod.event.K_KP_5,
  tcod.event.K_CLEAR,
}

CURSOR_Y_KEYS = {
  tcod.event.K_UP: -1,
  tcod.event.K_DOWN: 1,
  tcod.event.K_PAGEUP: -10,
  tcod.event.K_PAGEDOWN: 10,
}

class EventHandler(tcod.event.EventDispatch[Action]):
  def __init__(self, engine: Engine):
    self.engine = engine
    
  def handle_events(self, event: tcod.event.Event) -> None:
    self.handle_action(self.dispatch(event))
    
  def handle_action(self, action: Optional[Action]) -> bool:
    """
    handle actions returned from event methods
    return True if the action will advance a turn
    """
    if action is None:
      return False
    
    try:
      action.perform()
    except exceptions.Impossible as exc:
      self.engine.message_log.add_message(exc.args[0], color.impossible)
      return False # skip enemy turn on exceptions
    
    self.engine.handle_enemy_turns()
    
    self.engine.update_fov()
    return True

  def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
    raise SystemExit()
  
  def on_render(self, console: tcod.Console) -> None:
    self.engine.render(console)

class AskUserEventHandler(EventHandler):
  """ handles user input for actions which require special input """
  
  def handle_action(self, action: Optional[Action]) -> bool:
    """ return to the main event handler when a valid action was performed """
    if super().handle_action(action):
      self.engine.event_handler = MainGameHandler(self.engine)
      return True
    return False
  
  def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
    """ by default any key exits this input handler """
    if event.sym in { # ignore modifier keys
      tcod.event.K_LSHIFT,
      tcod.event.K_RSHIFT,
      tcod.event.K_LCTRL,
      tcod.event.K_RCTRL,
      tcod.event.K_LALT,
      tcod.event.K_RALT,
    }:
      return None
    return self.on_exit()
  
  def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> Optional[Action]:
    """ by default any mouse click exits this input handler """
    return self.on_exit()
  
  def on_exit(self) -> Optional[Action]:
    """ 
    called when the user is trying to exit or cancel an action
    by default this returns to the main event handler
    """
    self.engine.event_handler = MainGameHandler(self.engine)
    return None

class InventoryEventHandler(AskUserEventHandler):
  """
  this handler lets the user select an item
  what happens depends on the subclass
  """
  
  TITLE = "<missing title>"

  def on_render(self, console: tcod.console) -> None:
    """
    render an inventory meny, which displays the item in the inventory, and the letter to select them
    will move to a different position based on where the player is located, so the player can always see where they are
    """
    super().on_render(console)
    number_of_items_in_inventory = len(self.engine.player.inventory.items)
    
    height = number_of_items_in_inventory + 2
    
    if height <= 3:
      height = 3
      
    if self.engine.player.x <= 30:
      x = 40
    else:
      x = 0
    
    y = 0
    
    width = len(self.TITLE) + 4
    
    console.draw_frame(
      x=x,
      y=y,
      width=width,
      height=height,
      title=self.TITLE,
      clear=True,
      fg=(255, 255, 255),
      bg=(0, 0, 0),
    )
    
    if number_of_items_in_inventory > 0:
      for i, item in enumerate(self.engine.player.inventory.items):
        item_key = chr(ord("a") + i)
        console.print(x + 1, y + 1, f"({item_key}) {item.name}")
    
    else:
      console.print(x + 1, y + 1, "(Empty)")
  
  def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
    player = self.engine.player
    key = event.sym
    index = key - tcod.event.K_a

    if 0 <= index <= 26:
      try:
        selected_item = player.inventory.items[index]
      except IndexError:
        self.engine.message_log.add_message("Invalid entry", color.invalid)
        return None
      return self.on_item_selected(selected_item)
    return super().ev_keydown(event)
  
  def on_item_selected(self, item: Item) -> Optional[Action]:
    """ called when the user selects a valid item """
    raise NotImplementedError()
  
class InventoryActivateHandler(InventoryEventHandler):
  """ handle using an inventory item """
  TITLE = "Select an item to use."
  
  def on_item_selected(self, item: Item) -> Optional[Action]:
    """ return the action for the selected item """
    return item.consumable.get_action(self.engine.player)

class InventoryDropHandler(InventoryEventHandler):
  """ handle dropping an inventory item """
  
  TITLE = "Select an item to drop."
  
  def on_item_selcted(self, item: Item) -> Optional[Action]:
    """ drop this item """
    return actions.DropItem(self.engine.player, item)
        
class MainGameHandler(EventHandler):      
  def ev_mousemotion(self, event: tcod.event.MouseMotion) -> None:
    if self.engine.game_map.in_bounds(event.tile.x, event.tile.y):
      self.engine.mouse_location = event.tile.x, event.tile.y

  def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
    action: Optional[Action] = None
    
    key = event.sym
    
    player = self.engine.player

    if key in MOVE_KEYS:
      dx, dy = MOVE_KEYS[key]
      action = BumpAction(player, dx, dy)
    elif key in WAIT_KEYS:
      action = WaitAction(player)
    
    elif key == tcod.event.K_ESCAPE:
      raise SystemExit()
    elif key == tcod.event.K_v:
      self.engine.event_handler = HistoryViewer(self.engine)
    
    elif key == tcod.event.K_g:
      action = PickupAction(player)
    elif key == tcod.event.K_i:
      self.engine.event_handler = InventoryActivateHandler(self.engine)
    elif key == tcod.event.K_d:
      self.engine.event_handler = InventoryDropHandler(self.engine)
      
    # no valid key was pressed
    return action

class GameOverEventHandler(EventHandler):
  def ev_keydown(self, event: tcod.event.KeyDown) -> None:
    if event.sym == tcod.event.K_ESCAPE:
      raise SystemExit()
  
class HistoryViewer(EventHandler):
  """ print the history on a larger window which can be navigated """
  def __init__(self, engine: Engine):
    super().__init__(engine)
    self.log_length = len(engine.message_log.messages)
    self.cursor = self.log_length - 1
    
  def on_render(self, console: tcod.Console) -> None:
    super().on_render(console) # draw the main state as the background
    
    log_console = tcod.Console(console.width - 6, console.height - 6)
    
    # draw a frame with a custom banner title
    log_console.draw_frame(0, 0, log_console.width, log_console.height)
    log_console.print_box(
      0, 0, log_console.width, 1, "-|Message History|-", alignment=tcod.CENTER
    )
    
    # render the message log using the cursor parameter
    self.engine.message_log.render_messages(
      log_console,
      1,
      1,
      log_console.width - 2,
      log_console.height - 2,
      self.engine.message_log.messages[: self.cursor + 1]
    )
    log_console.blit(console, 3, 3)
  
  def ev_keydown(self, event: tcod.event.KeyDown) -> None:
    # fancy conditional movement to make it feel right
    if event.sym in CURSOR_Y_KEYS:
      adjust = CURSOR_Y_KEYS[event.sym]
      if adjust > 0 and self.cursor == 0:
        # only move from the top to the bottom when you're on the edge
        self.cursor = self.log_length - 1
      elif adjust > 0 and self.cursor == self.log_length - 1:
        # same with bottom to top movement
        self.cursor = 0
      else:
        # otherwise move while staying clamped to the bounds of the history log
        self.cursor = max(0, min(self.cursor + adjust, self.log_length - 1))
    elif event.sym == tcod.event.K_HOME:
      self.cursor = 0 # move directly to the top message
    elif event.sym == tcod.event.K_END:
      self.cursor = self.log_length - 1 # move directly to the last message
    else: # any other key moves back to the main game state
      self.engine.event_handler = MainGameHandler(self.engine)