package assignment1;

import assignment1.Game.SkillLevel;

public class Main {

	public static void main(String[] args) {
		
		//for (SkillLevel skill : SkillLevel.values()) {
		for (SkillLevel skill : new SkillLevel[] {SkillLevel.RANDOM}) {
			int gamesToPlay = 1;
			int firstWon = 0;
			int secondWon = 0;
			int ties = 0;

			for (int i = 0; i < gamesToPlay; i++) {
				Game game = new Game();
				game.setSkillLevel(skill);
				game.setVerbose(gamesToPlay == 1);
				game.play();

				Player winner = game.getWinner();
				if (winner == null) {
					ties++;
				}
				else if (winner == Player.FIRST) {
					firstWon++;
				}
				else if (winner == Player.SECOND) {
					secondWon++;
				}
			}

			System.out.println(gamesToPlay + " games played at skill level " + skill);
			System.out.println("First\t" + firstWon);
			System.out.println("Second\t" + secondWon);
			System.out.println("Tied\t" + ties);
		}
	}

}
