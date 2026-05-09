
require 'io/console'
require_relative '../Irrgarten/directions.rb'
require_relative '../Irrgarten/game_state'

module UI

  class TextUI

    #https://gist.github.com/acook/4190379
    def read_char
      STDIN.echo = false
      STDIN.raw!
    
      input = STDIN.getc.chr
      if input == "\e" 
        input << STDIN.read_nonblock(3) rescue nil
        input << STDIN.read_nonblock(2) rescue nil
      end
    ensure
      STDIN.echo = true
      STDIN.cooked!
    
      return input
    end

    def next_move
      print "Where? "
      got_input = false
      while (!got_input)
        c = read_char
        case c
          when "w"
            puts "UP ARROW"
            output = Directions::UP
            got_input = true
          when "s"
            puts "DOWN ARROW"
            output = Directions::DOWN
            got_input = true
          when "d"
            puts "RIGHT ARROW"
            output = Directions::RIGHT
            got_input = true
          when "a"
            puts "LEFT ARROW"
            output = Directions::LEFT
            got_input = true
          when "\u0003"
            puts "CONTROL-C"
            got_input = true
            exit(1)
          else
            #Error
        end
      end
      output
    end

    def show_game(game_state)
      puts game_state.monsters
      puts game_state.players
      puts game_state.labyrinth
      puts game_state.winner
      puts game_state.log

      if game_state.winner
        puts "Felicidades jugador #{game_state.current_player} has ganado la partida."
      else
        puts "Es el turno del jugador #{game_state.current_player}."
      end

    end

  end # class   

end # module   


