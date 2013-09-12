package assignment1;

public enum Property {

	SOLID, HOLLOW,
	BIG, SMALL,
	ROUND, SQUARE,
	RED, BLUE;

	public Property negate() {
		switch (this) {
			case SOLID:
				return HOLLOW;
			case HOLLOW:
				return SOLID;
			case BIG:
				return SMALL;
			case SMALL:
				return BIG;
			case ROUND:
				return SQUARE;
			case SQUARE:
				return ROUND;
			case RED:
				return BLUE;
			case BLUE:
				return RED;
			default:
				throw new RuntimeException();
		}
	}

}
