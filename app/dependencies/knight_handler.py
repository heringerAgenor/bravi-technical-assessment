
class KnightHandler():

    def __init__(self):
        self.COLUMNS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

    def predict_knight_positions(self, row: int, column: str):
        return self._predict_second_turn(self._predict_positions(row, column))


    def _predict_second_turn(self, first_turn_positions: dict):
        result = {"first_turn": first_turn_positions, "second_turn": []}
        for position in first_turn_positions:
            result["second_turn"].append({position: self._predict_positions(int(position[1]), position[0])})
        return result


    def _predict_positions(self, row: int, column: str):
        positions = []
        column_index = self.COLUMNS.index(column)

        for possible_position in self._knight_possible_positions(row, column_index + 1):
            if possible_position[0] <= 8 and possible_position[0] > 0 and possible_position[1] > 0 :
                try:
                    positions.append(f'{self.COLUMNS[possible_position[1] - 1]}{possible_position[0]}')
                except IndexError: 
                    continue
            
        return positions
    
    def _knight_possible_positions(self, row, column):
        return [
            (row - 2, column - 1),
            (row - 2, column + 1),
            (row + 2, column - 1),
            (row + 2, column + 1),
            (row - 1, column - 2),
            (row - 1, column + 2),
            (row + 1, column - 2),
            (row + 1, column + 2)
        ]




knight_handler = KnightHandler()
