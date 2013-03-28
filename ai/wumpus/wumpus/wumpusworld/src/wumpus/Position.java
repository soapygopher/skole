package wumpus;

import java.util.EnumSet;


public class Position {
	
	private EnumSet<State> states;

	public Position(EnumSet<State> states) {
		this.setStates(states);
	}

	public EnumSet<State> getStates() {
		return states;
	}

	public void setStates(EnumSet<State> states) {
		this.states = states;
	}

	@Override
	public String toString() {
		String out = "";
		for (State s : states) {
			out += s.name().charAt(0);
		}
		return out;
	}

}
