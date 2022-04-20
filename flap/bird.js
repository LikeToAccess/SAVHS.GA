function Bird() {
	this.y = height/2;
	this.x = 25
	this.diameter = 32;
	this.gravity = 0.7;
	this.lift = -25;
	this.vert_vel = 0;
	this.hori_vel = 0;
	this.max_speed = -15;
	this.color = "red";
	this.score = 0;

	this.show = function() {
		fill(this.color);
		ellipse(this.x, this.y, this.diameter);
	}

	this.up = function() {
		this.vert_vel += this.lift;
	}

	this.left = function() {
		this.hori_vel += -0.5;
	}

	this.right = function() {
		this.hori_vel += 0.5;
	}

	this.update = function() {
		this.vert_vel += this.gravity
		this.vert_vel *= 0.92
		this.hori_vel *= 0.92
		this.x += this.hori_vel;
		this.y += this.vert_vel;


		if (this.vert_vel <= this.max_speed) {
			this.vert_vel = this.max_speed;
		}
		if (this.y >= height - this.diameter/2) {
			this.y = height - this.diameter/2
			this.vert_vel = 0;
		}
		if (this.y <= this.diameter/2) {
			this.y = this.diameter/2
			this.vert_vel = 0;
		}
	}
}