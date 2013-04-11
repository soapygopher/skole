package wumpus;

import wumpus.Position;

public class Agent {

	public enum Direction {
		NORTH, SOUTH, EAST, WEST
	}
	
	public enum Turn {
		LEFT, RIGHT
	}

	private int x;
	private int y;
	private Direction facingDir;
	private boolean hasGold;
	private int arrows;


	public Agent(int x, int y, Direction facingDir, int arrows) {
		this.setX(x);
		this.setY(y);
		this.setFacingDir(facingDir);
		this.setHasGold(false);
		this.setArrows(arrows);
	}

	/**Change the facing direction of agent using turn left/right action
	 * 
	 * @param dir
	 * 		Direction to turn towards (LEFT/RIGHT)
	 */
	public void turn(Turn dir) {
		facingDir = getFacingDir();
		if (facingDir.equals(Direction.NORTH)) {
			facingDir = dir.equals(Turn.LEFT)? Direction.WEST:Direction.EAST; 
		}
		else if (facingDir.equals(Direction.SOUTH)) {
			facingDir = dir.equals(Turn.LEFT)? Direction.EAST:Direction.WEST;
		}
		else if (facingDir.equals(Direction.EAST)) {
			facingDir = dir.equals(Turn.LEFT)? Direction.NORTH:Direction.SOUTH;
		}
		else if (facingDir.equals(Direction.WEST)) {
			facingDir = dir.equals(Turn.LEFT)? Direction.SOUTH:Direction.NORTH;
		}
	}
	
	
	
	/**
	 * Move agent to the next block depending on which direction
	 *  it is facing but not outside the board.
	 *  The height and width parameters allow to keep the agent within the board.
	 *  Also helps to implement the bounce off the wall.
	 * @param height
	 * 		The height of the board
	 * @param width
	 * 		The width of the board
	 */
	public void moveForward (Position[][] playerBoard)   {		
		
		int height = playerBoard.length;
		int width = playerBoard[0].length;		
		x = getX();
		y = getY();
		facingDir = getFacingDir();		
		if (facingDir.equals(Direction.NORTH)) {
			facingDir = (y>0) ? Direction.NORTH : Direction.SOUTH;
			y = (y>0) ? (y-1): y;			 
			this.setX(x);
			this.setY(y);
			this.setFacingDir(facingDir);
		}
		else if (facingDir.equals(Direction.SOUTH)) {
			facingDir = (y<(height-1)) ? Direction.SOUTH : Direction.NORTH;
			y = (y<(height-1)) ? (y+1): y;			 
			this.setX(x);
			this.setY(y);			
			this.setFacingDir(facingDir);
		}
		else if (facingDir.equals(Direction.EAST)) {
			facingDir = (x<(width-1)) ? Direction.EAST : Direction.WEST;
			x = (x<(width-1)) ? (x+1):x;
			this.setX(x);
			this.setY(y);	
			this.setFacingDir(facingDir);
		}
		else if (facingDir.equals(Direction.WEST)) {
			facingDir = (x>0) ? Direction.WEST : Direction.EAST;
			x = (x>0) ? (x-1):x;			
			this.setX(x);
			this.setY(y);	
			this.setFacingDir(facingDir);
		}
	}
	
	public void grabGold () {
		setHasGold(true);
	}
	
	public Direction getFacingDir() {
		return facingDir;
	}


	public void setFacingDir(Direction facingDir) {
		this.facingDir = facingDir;
	}


	public int getY() {
		return y;
	}


	public void setY(int y) {
		this.y = y;
	}


	public int getX() {
		return x;
	}


	public void setX(int x) {
		this.x = x;
	}

	public boolean getHasGold() {
		return hasGold;
	}

	public void setHasGold(boolean hasGold) {
		this.hasGold = hasGold;
	}

	public int getArrows() {
		return arrows;
	}

	public void setArrows(int arrows) {
		this.arrows = arrows;
	}

}
