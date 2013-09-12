package assignment1;

import java.util.List;

public abstract class Utils {

	public static String printBoard(Piece[][] board) {
		String result = "";
		for (Piece[] line : board) {
			for (Piece piece : line) {
				if (piece != null) {
					result += piece.toString() + " ";
				}
				else {
					result += "____ ";
				}
			}
			result += "\n\n";
		}
		return result.trim();
	}


	public static String printPieces(List<Piece> pieces) {
		String result = "";
		for (int i = 0; i < pieces.size(); i++) {
			result += i + ": " + pieces.get(i);
			result += " - " + pieces.get(i).getProperties().toString().toLowerCase() + "\n";
		}
		return result;
	}


	public static Piece[][] transpose(Piece[][] board) {
		Piece[][] newBoard = new Piece[4][4];
		for (int i = 0; i < 4; i++) {
			for (int j = 0; j < 4; j++) {
				newBoard[i][j] = board[j][i];
			}
		}
		return newBoard;
	}

}
