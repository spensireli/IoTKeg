from pyfirmata import Arduino, util, STRING_DATA

class Lcd:
    def initialize_board(board):
        print('initializing board...')
        try:
            return(Arduino(board))
        except Error as e:
            print(e)

    def write_text(board, text):
        print('writing text')
        board.send_sysex( STRING_DATA, util.str_to_two_byte_iter(text) )


# # board = Arduino('/dev/ttyACM0')
# if __name__ == "__main__":
#     text = 'the state itself is flawed'
#     init_board = Lcd.initialize_board(board='/dev/ttyACM1')
#     write_text = Lcd.write_text(init_board, text)

