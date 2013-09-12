package assignment1;

public enum Player {

	FIRST, SECOND;

	public static final Player MAX_PLAYER = FIRST;
	public static final Player MIN_PLAYER = SECOND;
	private boolean human;

	static {
		FIRST.setHuman(false);
		SECOND.setHuman(false);
	}


	public Player other() {
		switch (this) {
			case FIRST:
				return SECOND;
			case SECOND:
				return FIRST;
			default:
				throw new RuntimeException();
		}
	}


	public boolean isHuman() {
		return human;
	}


	public void setHuman(boolean human) {
		this.human = human;
	}

}
