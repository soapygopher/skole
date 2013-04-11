package wumpus;

import java.util.EnumSet;
import wumpus.State;

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
			if (s.name() == "POSSIBLY_PIT") {
				out += 'p';
				continue;
			}
			if (s.name() == "POSSIBLY_WUMPUS") {
				out += 'w';
				continue;
			}
			if (s.name() == "NO_WUMPUS" || s.name() == "NO_PIT") {
				out += 'N';
				continue;
			}
			if (s.name() == "NO_PIT") {
				out += 'n';
				continue;
			}
			out += s.name().charAt(0);
		}
		
		return out;
	}

}
