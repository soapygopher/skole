package wumpus;

import java.util.ArrayList;
import java.util.EnumSet;
import java.util.List;
import java.util.Random;
import java.util.Scanner;

import wumpus.Agent.Direction;
import wumpus.Agent.Turn;

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
				
		int row = 0;
		int col = 0;
		
		Position[][] board = new Position[height][width];
		Random randGen = new Random();
		
		if (wumpuses ==0 && pits == 0)   {
			goldPlaced = true;			
		}
		
		for (int i = 0; i < height; i++) {
			for (int j = 0; j < width; j++) {			
			board[i][j] = new Position(EnumSet.noneOf(State.class));			
			}				
		}
		
		while (wumpusesPlaced < wumpuses)  {
			//Randomly generate index positions for wumpuses
			row = randGen.nextInt(height);
			col = randGen.nextInt(width);
			//Check if position already contains any wumpus
			Position current = board[row][col];
			if(current.getStates().contains(State.WUMPUS) || (row <2 && col<2)) {
				continue;
			} 
				board[row][col] = new Position(EnumSet.of(State.WUMPUS));
				wumpusesPlaced++;
		}
		
		while (pitsPlaced < pits)  {
			//Randomly generate index positions for pits
			row = randGen.nextInt(height);
			col = randGen.nextInt(width);
			//Check if position already contains any wumpus or pits
			Position current = board[row][col];
			if(current.getStates().contains(State.WUMPUS) 
					|| current.getStates().contains(State.PIT)
					|| (row <2 && col<2)) {
				continue;				
			} 
			board[row][col] = new Position(EnumSet.of(State.PIT));
			pitsPlaced++;			
		}

		while(!goldPlaced)  {
			row = randGen.nextInt(height);
			col = randGen.nextInt(width);
			//Check if position already contains any wumpus or pits
			Position current = board[row][col];
			if(current.getStates().contains(State.WUMPUS) 
					|| current.getStates().contains(State.PIT)
					|| (row <2 && col <2)){ 
				continue;				
			}
			board[row][col] = new Position(EnumSet.of(State.GOLD));
			goldPlaced = true;			
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
				int paddingSpaces = 6 - board[i][j].getStates().size();
				String padding = new String(new char[paddingSpaces]).replace('\0', ' ');
				if (board[i][j].getStates().size() == 0) {
					sb.append("    _  ");
				}
				else {
					sb.append(padding + board[i][j] + " ");
				}
			}
			sb.append("\n\n");
		}
		System.out.println(sb.toString());
	}
	
	@SuppressWarnings("unused")
	private static List<State> sense(Position[][] board, int x, int y) {
		List<State> perceptions = new ArrayList<State>();
		Position pos = board[y][x];
		for (State s : pos.getStates()) {
			perceptions.add(s);
		}
		return perceptions;
	}
	
	/**
	 * Get perception of current state from the real board and add that to the player's board.
	 * If there is a breeze or a stench, also added possible pits or possible wumpuses appropriately.
	 * @param player
	 * 			The agent
	 * @param realBoard
	 * 			The actual game environment
	 * @param playerBoard
	 * 			The environment in terms of the agent's perspective
	 * @return
	 * 			Updated agent environment
	 */
	private static Position[][] perceive(Agent player, Position[][] realBoard, Position[][] playerBoard)   {
		
		int i = player.getY();
		int j = player.getX();
		int height = realBoard.length;
		int width = realBoard[0].length;	
		Position[] neighbors = new Position[4];
		neighbors[0] = (i > 0) ? playerBoard[i - 1][j] : null; // north
		neighbors[1] = (j > 0) ? playerBoard[i][j - 1] : null; // west
		neighbors[2] = (i < height - 1) ? playerBoard[i + 1][j] : null; // south
		neighbors[3] = (j < width - 1) ? playerBoard[i][j + 1] : null; // east
		
		
		if (realBoard[i][j].getStates().contains(State.BREEZE)) {
			playerBoard[i][j].getStates().add(State.BREEZE);
			for (Position p : neighbors) {
				if (p != null 
						&& !p.getStates().contains(State.EXPLORED)
						&& !p.getStates().contains(State.NO_PIT)
						&& !p.getStates().contains(State.PIT)) {
					p.getStates().add(State.POSSIBLY_PIT);					
				}
							
			}
			
		}
		
		if (realBoard[i][j].getStates().contains(State.STENCH)) {
			playerBoard[i][j].getStates().add(State.STENCH);
			for (Position p : neighbors) {
				if (p != null 
						&& !p.getStates().contains(State.EXPLORED)
						&& !p.getStates().contains(State.NO_WUMPUS)
						&& !p.getStates().contains(State.WUMPUS)) {
					p.getStates().add(State.POSSIBLY_WUMPUS);			
				}
				
			}
		}
		
		if (realBoard[i][j].getStates().contains(State.GOLD)) {
			playerBoard[i][j].getStates().add(State.GOLD);
		}
	
		return playerBoard;
	}
	
	/**
	 * Check to see, if it is safe to move to the state that the agent is currently facing.
	 * A possible wumpus or possible pit state is considered unsafe.
	 * @param player
	 * 			The agent, required for its current position in the board
	 * @param playerBoard
	 * 			The agent's current view of the environment
	 * @return
	 * 			Boolean true/false to indicate safe or not.
	 */
	private static boolean safe (Agent player, Position[][] playerBoard) {
		
		boolean safe = true;
		Agent dummy = new Agent(player.getX(),player.getY(),player.getFacingDir(),player.getArrows());
		dummy.moveForward(playerBoard);
		int row = dummy.getY();
		int col = dummy.getX();		
		
		if (playerBoard[row][col].getStates().contains(State.POSSIBLY_WUMPUS)
				||playerBoard[row][col].getStates().contains(State.POSSIBLY_PIT)){
			safe = false;
		}
		if (playerBoard[row][col].getStates().contains(State.WUMPUS)
				||playerBoard[row][col].getStates().contains(State.PIT)){
			safe = false;
		}
		return safe;
	}
	/**Checks to see if the next state, that the agent is facing, has been explored
	 * 
	 * @param player
	 * 			The agent, required for its position and orientation
	 * @param playerBoard
	 * 			The agent's perception of the board
	 * @return
	 * 			Boolean true/false for explored/not_explored
	 */
	private static boolean explored(Agent player, Position[][] playerBoard) {
		
		boolean explored = false;
		Agent dummy = new Agent(player.getX(),player.getY(),player.getFacingDir(),player.getArrows());
		dummy.moveForward(playerBoard);
		int row = dummy.getY();
		int col = dummy.getX();		
		
		if (playerBoard[row][col].getStates().contains(State.EXPLORED)){
			explored = true;
		}		
		return explored;
	}
	/**
	 * Finds an appropriate direction to face for the next moveForward.
	 * States that have not been explored and considered safe are given highest priority.
	 * If no such state is found, previously explored safe states are chosen.
	 * This function ensures that the agent never goes to states that are possibly_pit/wumpus
	 * @param player
	 * 			The agent, required to find its facing direction 
	 * @param playerBoard
	 * 			The agent's perception of the board
	 * @return
	 * 			Returns the agent with an updated facingDirection
	 */
	private static Agent findNextMove(Agent player, Position[][] playerBoard) {
		
		Random randGen = new Random();
		int r=0;
		
		for (int i=0; i<4; i++) {
			if (!explored(player,playerBoard) && safe(player,playerBoard)) {
				return player;
			}
			player.turn(Turn.RIGHT);
			System.out.println("Action -> TURN RIGHT");
		}//if no return then ends with player facing original direction
		r = randGen.nextInt(4);
		for (int i=0; i<r;i++){
			player.turn(Turn.RIGHT);
			System.out.println("Action -> TURN RIGHT");
		}		
		while (!safe(player,playerBoard)) {
			r = randGen.nextInt(4);
			for (int i=0; i<r;i++){
				player.turn(Turn.RIGHT);
				System.out.println("Action -> TURN RIGHT");
			}
		}
		
		// Make a random selection for the state to track back to
		
		return player;		
	}
	/**
	 * Try to deduce the location of pits and wumpuses from current knowledge.
	 * If a possibly_pit/wumpus state was previously explored those states are cleared
	 * If any neighbors of a possibly_pit state does not contain a breeze, the state is cleared
	 * If any neighbors of a possibly_wumpus state does not contain a stench, the state is cleared 
	 * @param playerBoard
	 * 			Current knowledge about the environment
	 * @return
	 * 			Updated board after inferences
	 */
	private static Position[][] inference(Position[][] playerBoard) {
		
		int height = playerBoard.length;
		int width = playerBoard[0].length;
		
		
		for (int i=0; i<height; i++){
			for (int j=0; j<width; j++) {
				
				Position here = playerBoard[i][j];
				
				Position[] neighbors = new Position[4];
				neighbors[0] = (i > 0) ? playerBoard[i - 1][j] : null; // north
				neighbors[1] = (j > 0) ? playerBoard[i][j - 1] : null; // west
				neighbors[2] = (i < height - 1) ? playerBoard[i + 1][j] : null; // south
				neighbors[3] = (j < width - 1) ? playerBoard[i][j + 1] : null; // east
				
				if (here.getStates().contains(State.KILLED_WUMPUS)) {
					here.getStates().remove(State.POSSIBLY_WUMPUS);
					here.getStates().remove(State.WUMPUS);
					here.getStates().remove(State.POSSIBLY_PIT);
					here.getStates().remove(State.PIT);
				}		
			
				
				if (here.getStates().contains(State.POSSIBLY_PIT)) {
					
					if (here.getStates().contains(State.EXPLORED)) {
						here.getStates().remove(State.POSSIBLY_PIT);
						here.getStates().remove(State.NO_PIT);
					}
					else {
						
						
						for (Position p : neighbors) {
							if (p != null) {	//States adjacent to possibly pit doesn't have breeze, then remove possibly pit
								if (p.getStates().contains(State.EXPLORED) 
										&& !p.getStates().contains(State.BREEZE)) {
									here.getStates().remove(State.POSSIBLY_PIT);
									here.getStates().add(State.NO_PIT);
								}
								
							}
						}
						
					}
					
				}
				
				if (here.getStates().contains(State.POSSIBLY_WUMPUS)) {
					
					if (here.getStates().contains(State.EXPLORED)) {
						here.getStates().remove(State.POSSIBLY_WUMPUS);
						here.getStates().add(State.NO_WUMPUS);
					}
					else {
												
						for (Position p : neighbors) {
							if (p != null) {
								if (p.getStates().contains(State.EXPLORED) 
										&& !p.getStates().contains(State.STENCH)) {
									here.getStates().remove(State.POSSIBLY_WUMPUS);
									here.getStates().remove(State.NO_WUMPUS);	
								}	
								
							}
						}
						
					}
					
				}
				
				
			}
		}
		
		for (int i=0; i<height; i++){
			for (int j=0; j<width; j++) {
				
				Position here = playerBoard[i][j];
				int pitCount = 0;
				int wumpusCount = 0;
				int index=0;
				int count;
				count = 0;
				pitCount = 0;
				Position[] neighbors = new Position[4];
				neighbors[0] = (i > 0) ? playerBoard[i - 1][j] : null; // north
				neighbors[1] = (j > 0) ? playerBoard[i][j - 1] : null; // west
				neighbors[2] = (i < height - 1) ? playerBoard[i + 1][j] : null; // south
				neighbors[3] = (j < width - 1) ? playerBoard[i][j + 1] : null; // east
				if (here.getStates().contains(State.BREEZE)) {
					for (Position p:neighbors){
						if (p!=null 
								&& (p.getStates().contains(State.POSSIBLY_PIT)
										|| p.getStates().contains(State.PIT))) {
							pitCount++;
							index = count;
							continue;
						}
						count++;
					}
					if (pitCount == 1) {
						Position p = neighbors[index];
						p.getStates().remove(State.POSSIBLY_PIT);
						p.getStates().add(State.PIT);
						try {
							p.getStates().remove(State.POSSIBLY_WUMPUS);							
						}
						catch (NullPointerException e) {} // don't care
						try {							
							p.getStates().remove(State.WUMPUS);
						}
						catch (NullPointerException e) {} // don't care
					}
					
				}
				count = 0;
				wumpusCount = 0;
				if (here.getStates().contains(State.STENCH)) {
					for (Position p:neighbors){
						if (p!=null 
								&& (p.getStates().contains(State.POSSIBLY_WUMPUS)
										|| p.getStates().contains(State.WUMPUS))) {
							wumpusCount++;
							index = count;
							continue;
						}
						count++;
					}
					if (wumpusCount == 1) {
						Position p = neighbors[index];
						p.getStates().remove(State.POSSIBLY_WUMPUS);
						p.getStates().add(State.WUMPUS);
						try {
							p.getStates().remove(State.POSSIBLY_PIT);							
						}
						catch (NullPointerException e) {} // don't care
						try {							
							p.getStates().remove(State.PIT);
						}
						catch (NullPointerException e) {} // don't care
					}
					
				}
			}
		}
		return playerBoard;
	}
	
	/**Checks if the agent is in the same row/col as the wumpus
	 * 
	 * @param player
	 * 			The agent
	 * @param playerBoard
	 * 			The agent's perception of the board
	 * @return
	 * 			The location of the wumpus if found
	 * 			Null otherwise
	 */
	
	private static int[] alignedWithWumpus(Agent player, Position[][] playerBoard) {
		
		int height = playerBoard.length;
		int width = playerBoard[0].length;
		int row = player.getY();
		int col = player.getX();
		int[] wumpusLocation = new int[2]; //row and col values of wumpus
		
		for (int i = 0; i<width; i++) {
			if(playerBoard[row][i].getStates().contains(State.WUMPUS)){
				wumpusLocation[0] = row;
				wumpusLocation[1] = i;
				return wumpusLocation;
			}
		}
		for (int i = 0; i<height; i++) {
			if(playerBoard[i][col].getStates().contains(State.WUMPUS)){
				wumpusLocation[0] = i;
				wumpusLocation[1] = col;
				return wumpusLocation;
			}
		}
		
		return null;
	}
	
	private static Agent faceWumpus(Agent player, int[] wumpusLocation) {
		
		int row = player.getY();
		int col = player.getX();
		int wumpusRow = wumpusLocation[0];
		int wumpusCol = wumpusLocation[1];
		
		if (row == wumpusRow){
			if (col < wumpusCol){
				while(player.getFacingDir() != Direction.EAST){
					player.turn(Turn.RIGHT);
					System.out.println("Action -> TURN RIGHT");
				}
				return player;
			}
			else {
				while(player.getFacingDir() != Direction.WEST){
					player.turn(Turn.RIGHT);
					System.out.println("Action -> TURN RIGHT");
				}
				return player;
			}
		}
		
		else if (col == wumpusCol){
			if (row < wumpusRow){
				while(player.getFacingDir() != Direction.SOUTH){
					player.turn(Turn.RIGHT);
					System.out.println("Action -> RIGHT");
				}
				return player;
			}
			else {
				while(player.getFacingDir() != Direction.NORTH){
					player.turn(Turn.RIGHT);
					System.out.println("Action -> RIGHT");
				}
				return player;
			}
		}
		
		return player;
	}
	
	private static void killWumpus(int[] wumpusLocation, Position[][] realBoard) {
		
		if (realBoard[wumpusLocation[0]][wumpusLocation[1]].getStates().contains(State.WUMPUS)){
			scream = true;
		}			
		
	}
	
	private static Position[][] updatePlayerBoard(Position[][] playerBoard,
			int[] wumpusLocation) {
		
		int height = playerBoard.length;
		int width = playerBoard[0].length;
		
		int row = wumpusLocation[0];
		int col = wumpusLocation[1];
		
		playerBoard[row][col].getStates().remove(State.WUMPUS);
		playerBoard[row][col].getStates().add(State.KILLED_WUMPUS);
		Position[] neighbors = new Position[4];
		neighbors[0] = (row > 0) ? playerBoard[row - 1][col] : null; // north
		neighbors[1] = (col > 0) ? playerBoard[row][col - 1] : null; // west
		neighbors[2] = (row < height - 1) ? playerBoard[row + 1][col] : null; // south
		neighbors[3] = (col < width - 1) ? playerBoard[row][col + 1] : null; // east
		for (Position p:neighbors) {
			if(p!=null 
					&& p.getStates().contains(State.STENCH)){
				p.getStates().remove(State.EXPLORED);
				p.getStates().remove(State.STENCH);
			}
		}
		
		
		return playerBoard;
	}


	private static Position[][] updateRealBoard(Position[][] realBoard,
			int[] wumpusLocation) {
		
		int height = realBoard.length;
		int width = realBoard[0].length;
		
		int row = wumpusLocation[0];
		int col = wumpusLocation[1];
		
		realBoard[row][col].getStates().remove(State.WUMPUS);
		Position[] neighbors = new Position[4];
		neighbors[0] = (row > 0) ? realBoard[row - 1][col] : null; // north
		neighbors[1] = (col > 0) ? realBoard[row][col - 1] : null; // west
		neighbors[2] = (row < height - 1) ? realBoard[row + 1][col] : null; // south
		neighbors[3] = (col < width - 1) ? realBoard[row][col + 1] : null; // east
		for (Position p:neighbors) {
			if(p!=null){
				p.getStates().remove(State.STENCH);
			}
		}
		
		for (int i=0; i<height; i++){
			for (int j=0; j<width; j++) {
				if (realBoard[i][j].getStates().contains(State.WUMPUS)) {					
					Position[] neighbor = new Position[4];
					neighbor[0] = (i > 0) ? realBoard[i - 1][j] : null; // north
					neighbor[1] = (j > 0) ? realBoard[i][j - 1] : null; // west
					neighbor[2] = (i < height - 1) ? realBoard[i + 1][j] : null; // south
					neighbor[3] = (j < width - 1) ? realBoard[i][j + 1] : null; // east
					for (Position p: neighbor) {
						if (p!= null 
								&& !p.getStates().contains(State.STENCH)){
							p.getStates().add(State.STENCH);
						}
					}
				}
				
			}
		}
		
		return realBoard;
	}
	
	
	// GLOBAL VARIABLES
	static boolean scream = false;	
	
	/**
	 * @param args
	 */
	@SuppressWarnings({ "unused", "resource" })
	public static void main(String[] args) {

		int width = 5;
		int height = 5;
		int wumpuses = 2;
		int pits = 3;
		int[] wumpusLocation = new int[2];
		
		Scanner input = new Scanner(System.in);
		String response;
		
		Position[][] realBoard = initBoard(height, width, wumpuses, pits);
		printBoard(realBoard);		
				
		//Generate empty states representing the agents perception
		Position[][] playerBoard = initBoard(height,width,0,0);
		
		//Initialize Agent
		Agent player = new Agent(0, 0, Direction.EAST,wumpuses);
		playerBoard[player.getY()][player.getX()].getStates().add(State.AGENT);
		playerBoard[player.getY()][player.getX()].getStates().add(State.EXPLORED);
		printBoard(playerBoard);
		//System.out.println(player.getX() + " " + player.getY()+" "+player.getFacingDir());
				
		while (!player.getHasGold()) {
			
			System.out.println("Hit return to continue!"); //Just to pause execution
			response = input.nextLine();
			
			playerBoard[player.getY()][player.getX()].getStates().remove(State.AGENT);  
				
			player = findNextMove(player,playerBoard);// find which direction to face
			System.out.println("\nPrevious State \n Location["+player.getX()+
					"," + player.getY()+"] Facing '"+player.getFacingDir()+"'\n");
			player.moveForward(playerBoard);
			System.out.println("Action -> MOVE FORWARD\n");
			playerBoard[player.getY()][player.getX()].getStates().add(State.AGENT);// add agent to new state
			
			System.out.println("Current State \n Location["+player.getX()+
					"," + player.getY()+"] Facing '"+player.getFacingDir()+"'\n\n");
			
			if (!playerBoard[player.getY()][player.getX()].getStates().contains(State.EXPLORED)) {
				playerBoard = perceive(player,realBoard,playerBoard);	
			}
			playerBoard[player.getY()][player.getX()].getStates().add(State.EXPLORED);
			
			
			
			if( (wumpusLocation = alignedWithWumpus(player,playerBoard)) != null 
					&& player.getArrows() > 0){				
				player = faceWumpus(player,wumpusLocation);
				System.out.println("*****		Facing Wumpus		*****");
				
				//printBoard(playerBoard);
				System.out.println("*****		Shoot Arrow		*****");				
				killWumpus(wumpusLocation, realBoard);
				player.setArrows(player.getArrows()-1);
				if(scream) {
					System.out.println("*****		SCREAM HEARD!!		*****");
					realBoard = updateRealBoard(realBoard,wumpusLocation);
					playerBoard = updatePlayerBoard(playerBoard,wumpusLocation);					
					scream = false;
				}
				else{
					playerBoard[wumpusLocation[0]][wumpusLocation[1]].getStates().remove(State.WUMPUS);
					playerBoard[wumpusLocation[0]][wumpusLocation[1]].getStates().add(State.NO_WUMPUS);
				}
					
				System.out.println("Current State \n Location["+player.getX()+
						"," + player.getY()+"] Facing '"+player.getFacingDir()+"'\n\n");
			}
			
		
			
			
			if(playerBoard[player.getY()][player.getX()].getStates().contains(State.GOLD)) {
				player.grabGold();
				printBoard(playerBoard);
				//break;
				continue;
			}
			
			playerBoard = inference(playerBoard);
			printBoard(playerBoard);						
			
		} 
		
		System.out.println("GAME OVER!!");
		
	}


	


	


	


	


	
}

