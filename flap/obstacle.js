function Obstacle () {
	this.top = random(100, height/2) - 50;
	this.bottom = random(100, height/2) - 50;
	this.x = width;
	this.w = 20;
	this.speed = 7;
	this.player_highlight = false;
	this.bot_highlight = false;


	this.hits = function(bird, bot) {
		if ((bird.y<this.top||bird.y>height-this.bottom) && (bird.x+bird.diameter/2>this.x&&bird.x+bird.diameter/2<this.x+this.w)) {
			this.player_highlight = true;
			return true;
		}
		if ((bot.y<this.top||bot.y>height-this.bottom) && (bot.x+bot.diameter/2>this.x&&bot.x+bot.diameter/2<this.x+this.w)) {
			this.bot_highlight = true;
		}
		return false;
	}

	this.show = function() {
		fill(255);
		if (this.player_highlight === true) {
			fill(255, 0, 0);
		}
		if (this.bot_highlight === true) {
			fill(0, 0, 255);
		}
		rect(this.x, -1, this.w, this.top);
		rect(this.x, height-this.bottom, this.w, this.bottom);
	}

	this.update = function() {
		this.x -= this.speed;
		this.speed += 0.15
	}
}