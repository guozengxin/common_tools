drop table if exists taskinfo;

create table taskinfo (
	id int(11) not null auto_increment,
	taskname varchar(64) not null,
	starttime datetime,
	endtime datetime,
	is_succeed tinyint(1),
	run_info varchar(2048),
	primary key (id)
);
