game_active = False
board = [' '] * 9
current_player = 'X'

async def start_game(content):
  global message = content
      if game_active:
          await message.channel.send('A game is already in progress.')
          return
  
      game_active = True
      board = [' '] * 9
      current_player = 'X'
      await display_board(message.channel)
  
  if game_active and content.isdigit() and 1 <= int(content) <= 9:
    move = int(content) - 1
    
      if board[move] == ' ':
          board[move] = current_player
          await display_board(message.channel)
          if await check_winner(current_player):
              await message.channel.send(f'Player {current_player} wins!')
              game_active = False
          else:
              current_player = 'O' if current_player == 'X' else 'X'
            

async def display_board(channel):
    board_text = ""
    for i in range(0, 9, 3):
        row = " | ".join(board[i:i + 3])
        board_text += f"{row}\n{'-'*9}\n"

    message = f"```\n{board_text}\n```"
    await channel.send(message)


async def check_winner(player):
    winning_combinations = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],  # Rows
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],  # Columns
        [0, 4, 8],
        [2, 4, 6]  # Diagonals
    ]

    return any(
        all(board[i] == player for i in combo) for combo in winning_combinations)
