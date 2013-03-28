package wumpus;

public class Agent {

	public enum Direction {
		NORTH, SOUTH, EAST, WEST
	}

	private int x;
	private int y;
	private Direction facingDir;


	public Agent(int x, int y, Direction facingDir) {
		this.setX(x);
		this.setY(y);
		this.setFacingDir(facingDir);
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

}
