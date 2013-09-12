package assignment1;

import java.util.Collections;
import java.util.EnumSet;
import java.util.Set;

public class Piece {

	private Set<Property> properties = EnumSet.noneOf(Property.class);


	public Piece(Property... props) {
		Collections.addAll(properties, props);
	}


	public Set<Property> getProperties() {
		return properties;
	}


	public void setProperties(Set<Property> properties) {
		this.properties = properties;
	}


	public String toString() {
		String result = "";

		if (properties.contains(Property.RED)) {
			result += "r";
		}
		else {
			result += "b";
		}
		
		if (properties.contains(Property.HOLLOW)) {
			result += "*";
		}
		else {
			result += " ";
		}

		if (properties.contains(Property.BIG)) {
			result = result.toUpperCase();
		}
		// else small, leave as is

		if (properties.contains(Property.ROUND)) {
			result = "(" + result + ")";
		}
		else {
			result = "[" + result + "]";
		}

		return result;
	}

}
