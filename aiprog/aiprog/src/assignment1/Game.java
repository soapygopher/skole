package assignment1;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;
import java.util.Scanner;

public class Game {

	public static enum SkillLevel {
		RANDOM, NOVICE, MINMAX_ALPHABETA
	}

	private Player currentPlayer = Player.FIRST;
	private List<Piece> pieces = new ArrayList<>();
	private Piece[][] board = new Piece[4][4];
	private Piece pieceToPlay;
	private SkillLevel skillLevel;
	private boolean verbose;
	private Player winner;


	public Game() {
		Collections.addAll(pieces, new Piece[] {
				new Piece(Property.RED, Property.ROUND, Property.HOLLOW, Property.SMALL),
				new Piece(Property.RED, Property.ROUND, Property.HOLLOW, Property.BIG),
				new Piece(Property.RED, Property.ROUND, Property.SOLID, Property.SMALL),
				new Piece(Property.RED, Property.ROUND, Property.SOLID, Property.BIG),
				new Piece(Property.RED, Property.SQUARE, Property.HOLLOW, Property.SMALL),
				new Piece(Property.RED, Property.SQUARE, Property.HOLLOW, Property.BIG),
				new Piece(Property.RED, Property.SQUARE, Property.SOLID, Property.SMALL),
				new Piece(Property.RED, Property.SQUARE, Property.SOLID, Property.BIG),
				new Piece(Property.BLUE, Property.ROUND, Property.HOLLOW, Property.SMALL),
				new Piece(Property.BLUE, Property.ROUND, Property.HOLLOW, Property.BIG),
				new Piece(Property.BLUE, Property.ROUND, Property.SOLID, Property.SMALL),
				new Piece(Property.BLUE, Property.ROUND, Property.SOLID, Property.BIG),
				new Piece(Property.BLUE, Property.SQUARE, Property.HOLLOW, Property.SMALL),
				new Piece(Property.BLUE, Property.SQUARE, Property.HOLLOW, Property.BIG),
				new Piece(Property.BLUE, Property.SQUARE, Property.SOLID, Property.SMALL),
				new Piece(Property.BLUE, Property.SQUARE, Property.SOLID, Property.BIG)
		});
		pieceToPlay = pieces.get(new Random().nextInt(pieces.size()));
		pieces.remove(pieceToPlay);
	}


	public void play() {
		if (verbose) {
			System.out.println("Player " + currentPlayer + " starts with piece " + pieceToPlay);
		}
		
		while (!Logic.winning(board, verbose)) {

			if (pieceToPlay == null) {
				if (verbose) {
					System.out.println("Game over, no more pieces");
				}
				setWinner(null);
				return;
			}
			else if (verbose) {
				System.out.println("=========================");
				System.out.println(currentPlayer + "'s turn");
			}

			if (currentPlayer.isHuman()) {
				userInput:
				try {
					handleUserInput();
				}
				catch (Exception e) {
					System.out.println("ERROR: " + e.getMessage());
					e.printStackTrace();
					break userInput; // uelegant, yuck
				}
			}
			else {
				computeAndMove(skillLevel);
			}

			if (verbose) {
				System.out.println("Current board:");
				System.out.println(Utils.printBoard(board));
			}

			currentPlayer = currentPlayer.other();
		}

		// ferdig med løkken, noen har vunnet
		if (verbose) {
			System.out.println("Player " + currentPlayer.other() + " won");
		}
		setWinner(currentPlayer.other());
	}


	private void handleUserInput() {
		@SuppressWarnings("resource")
		// ikke lukk, det lukker System.in og gir masse problemer
		Scanner scanner = new Scanner(System.in);

		System.out.println("Your piece is " + pieceToPlay.toString() +
				" with properties " + pieceToPlay.getProperties().toString().toLowerCase());

		System.out.println("Place at x =");
		int x = Integer.parseInt(scanner.nextLine());
		System.out.println("Place at y =");
		int y = Integer.parseInt(scanner.nextLine());
		if (board[y][x] != null) {
			throw new IllegalArgumentException("That position is occupied");
		}

		if (x >= 0 && x <= 3 && y >= 0 && y <= 3) {
			board[y][x] = pieceToPlay;
		}
		else {
			throw new IllegalArgumentException("Invalid position");
		}

		System.out.println(Utils.printBoard(board));
		System.out.println("Pick a piece for the opponent");
		System.out.println(Utils.printPieces(pieces));
		System.out.println("Opponent gets piece number");

		int nr = Integer.parseInt(scanner.nextLine());
		Piece newPieceToPlay = pieces.get(nr);
		System.out.println("The opponent gets " + newPieceToPlay + " with properties " + newPieceToPlay.getProperties());

		pieces.remove(newPieceToPlay);
		pieceToPlay = newPieceToPlay;

	}


	private void computeAndMove(SkillLevel skill) {
		if (skill == SkillLevel.RANDOM) {
			placeRandomly();
		}
		else if (skill == SkillLevel.NOVICE) {
			// TODO
		}
		else {
			// TODO
		}
	}


	private void placeRandomly() {
		Random randgen = new Random();
		int x;
		int y;
		
		do {
			x = randgen.nextInt(4);
			y = randgen.nextInt(4);
		}
		while (board[y][x] != null);

		board[y][x] = pieceToPlay;
		if (verbose) {
			System.out.println("Piece " + pieceToPlay + " was randomly placed at x = " + x + ", y = " + y);
		}

		Piece newPiece;
		if (pieces.size() == 0) {
			newPiece = null;
		}
		else {
			newPiece = pieces.get(randgen.nextInt(pieces.size()));
			pieces.remove(newPiece);
		}
		pieceToPlay = newPiece;
		if (verbose) {
			System.out.println("Opponent was randomly given piece " + newPiece);
		}
	}


	public boolean isVerbose() {
		return verbose;
	}


	public void setVerbose(boolean verbose) {
		this.verbose = verbose;
	}


	public Player getWinner() {
		return winner;
	}


	public void setWinner(Player winner) {
		this.winner = winner;
	}


	public SkillLevel getSkillLevel() {
		return skillLevel;
	}


	public void setSkillLevel(SkillLevel skillLevel) {
		this.skillLevel = skillLevel;
	}

}
