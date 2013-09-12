package assignment1;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public abstract class Logic {

	private static final int CUTOFF_DEPTH = 5;


	public static List<Piece[][]> successors(Piece[][] board, Piece pieceToPlace) {
		List<Piece[][]> succs = new ArrayList<>();
		for (int i = 0; i < board.length; i++) {
			for (int j = 0; j < board[i].length; j++) {
				Piece position = board[i][j];
				if (position == null) {
					Piece[][] newBoard = Arrays.copyOf(board, board.length);
					newBoard[i][j] = pieceToPlace;
					succs.add(newBoard);
				}
			}
		}
		return succs;
	}


	public static boolean winning(Piece[][] board, boolean verbose) {
		for (Property prop : Property.values()) {
			
			// horisontalt
			for (int i = 0; i < 4; i++) {
				if (sharesProperty(board[i], prop)) {
					if (verbose) {
						System.out.println("The pieces in row " + i + " share the property " + prop);
					}
					return true;
				}
			}
			
			// vertikalt
			Piece[][] transposed = Utils.transpose(board);
			for (int i = 0; i < 4; i++) {
				if (sharesProperty(transposed[i], prop)) {
					if (verbose) {
						System.out.println("The pieces in column " + i + " share the property " + prop);
					}
					return true;
				}
			}
			
			// diagonal nedover
			if (sharesProperty(new Piece[] {board[0][0], board[1][1], board[2][2], board[3][3]}, prop)) {
				if (verbose) {
					System.out.println("The pieces in the descending diagonal share the property " + prop);
				}
				return true;
			}
			
			// diagonal oppover
			if (sharesProperty(new Piece[] {board[3][0], board[2][1], board[1][2], board[0][3]}, prop)) {
				if (verbose) {
					System.out.println("The pieces in the ascending diagonal share the property " + prop);
				}
				return true;
			}
			
		}

		return false;
	}


	private static boolean sharesProperty(Piece[] pieces, Property prop) {
		boolean shared = true;
		for (Piece p : pieces) {
			if (p == null) {
				return false;
			}
			shared &= p.getProperties().contains(prop);
		}
		return shared;
	}


	public static long alphaBeta(Piece[][] board, Piece piecePlayed, Player player, int depth,
			long alpha, long beta) {
		
		// TODO

		if (depth >= CUTOFF_DEPTH) {
			return valuation(board, player);
		}
		

		List<Piece[][]> children = successors(board, piecePlayed);

		if (player.equals(Player.MAX_PLAYER)) {
			for (Piece[][] child : children) {
				// hva gjør man med piecePlayed?
				long candidateAlpha = alphaBeta(child, null, player.other(), depth + 1, alpha, beta);
				if (candidateAlpha > alpha) {
					alpha = candidateAlpha;
				}
				if (alpha >= beta) {
					return beta;
				}
			}
			return alpha;
		}
		else {
			for (Piece[][] child : children) {
				long candidateBeta = alphaBeta(child, null, player.other(), depth + 1, alpha, beta);
				if (candidateBeta < beta) {
					alpha = candidateBeta;
				}
				if (alpha >= beta) {
					return alpha;
				}
			}
			return beta;
		}
	}


	private static long valuation(Piece[][] board, Player player) {
		return 0; // TODO
	}
}
