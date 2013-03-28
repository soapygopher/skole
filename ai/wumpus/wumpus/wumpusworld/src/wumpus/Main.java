package wumpus;

import java.util.ArrayList;
import java.util.EnumSet;
import java.util.List;
import java.util.Random;

import wumpus.Agent.Direction;

public class Main {

	/**
	 * Initialize the board with the given dimensions and number of pits and
	 * wumpuses.
	 * 
	 * @param height
	 *            The height of the board.
	 * @param width
	 *            The width of the board.
	 * @param wumpuses
	 *            The number of wumpuses to place.
	 * @param pits
	 *            The number of pits to place.
	 * @return A height-by-width array of Positions, with pits and wumpuses
	 *         scattered randomly, and breezes and stenches in their neighboring
	 *         squares, respectively.
	 */
	private static Position[][] initBoard(int height, int width, int wumpuses, int pits) {
		int wumpusesPlaced = 0;
		int pitsPlaced = 0;
		boolean goldPlaced = false;
		double wumpusThreshold = (float) wumpuses / (width * height);
		double pitThreshold = (float) pits / (width * height);
		double goldThreshold = 1.0 / (width * height);

		Position[][] board = new Position[height][width];
		Random randGen = new Random();

		for (int i = 0; i < height; i++) {
			for (int j = 0; j < width; j++) {
				// Pits, wumpuses and gold are mutually exclusive
				if (randGen.nextDouble() < wumpusThreshold && wumpusesPlaced < wumpuses) {
					board[i][j] = new Position(EnumSet.of(State.WUMPUS));
					wumpusesPlaced++;
				}
				else if (randGen.nextDouble() < pitThreshold && pitsPlaced < pits) {
					board[i][j] = new Position(EnumSet.of(State.PIT));
					pitsPlaced++;
				}
				else if (randGen.nextDouble() < goldThreshold && !goldPlaced) {
					board[i][j] = new Position(EnumSet.of(State.GOLD));
					goldPlaced = true;
				}
				else {
					board[i][j] = new Position(EnumSet.noneOf(State.class));
				}
			}
		}

		// Place breezes and stenches according to where the pits and wumpuses are
		for (int i = 0; i < height; i++) {
			for (int j = 0; j < width; j++) {

				Position here = board[i][j];

				Position[] neighbors = new Position[4];
				neighbors[0] = (i > 0) ? board[i - 1][j] : null; // north
				neighbors[1] = (j > 0) ? board[i][j - 1] : null; // west
				neighbors[2] = (i < height - 1) ? board[i + 1][j] : null; // south
				neighbors[3] = (j < width - 1) ? board[i][j + 1] : null; // east

				for (Position p : neighbors) {
					if (p != null) {
						if (p.getStates().contains(State.WUMPUS)) {
							here.getStates().add(State.STENCH);
						}
						if (p.getStates().contains(State.PIT)) {
							here.getStates().add(State.BREEZE);
						}
					}
				}

			}
		}

		return board;
	}


	public static void printBoard(Position[][] board) {
		int height = board.length;
		int width = board[0].length;
		StringBuilder sb = new StringBuilder();
		for (int i = 0; i < height; i++) {
			for (int j = 0; j < width; j++) {
				// Bad padding algorithm, should be fixed
				int paddingSpaces = 3 - board[i][j].getStates().size();
				String padding = new String(new char[paddingSpaces]).replace('\0', ' ');
				if (board[i][j].getStates().size() == 0) {
					sb.append("  _ ");
				}
				else {
					sb.append(padding + board[i][j] + " ");
				}
			}
			sb.append("\n\n");
		}
		System.out.println(sb.toString());
	}
	
	private static List<State> sense(Position[][] board, int x, int y) {
		List<State> perceptions = new ArrayList<State>();
		Position pos = board[y][x];
		for (State s : pos.getStates()) {
			perceptions.add(s);
		}
		return perceptions;
	}


	/**
	 * @param args
	 */
	public static void main(String[] args) {

		int width = 4;
		int height = 4;
		int wumpuses = 1;
		int pits = 3;

		Position[][] realBoard = initBoard(height, width, wumpuses, pits);
		Position[][] playerBoard = new Position[height][width];
		Agent player = new Agent(0, 0, Direction.EAST);
		
		//do {
			List<State> perceptions = sense(playerBoard, player.getX(), player.getY());
			
		//}
		//while (true);
		

		printBoard(realBoard);

	}

}
