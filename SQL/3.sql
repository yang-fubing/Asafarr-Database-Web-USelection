use dbpj;

create or replace view candidate_list as select name, party from votedb_candidate;

DELIMITER //  
create function aggregation_state_vote(name varchar(50)) Returns INT
Begin
	DECLARE s INT DEFAULT 0;

	select sum(votes)
	INTO s
	from votedb_state_vote
	where state_id = name
	group by state_id;

	return s;
end;
//  
DELIMITER ;



DELIMITER //  
CREATE PROCEDURE renew_state_total_vote(IN name varchar(50))
BEGIN
    DECLARE s INT DEFAULT 0;

    SET s = aggregation_state_vote(name);

	update votedb_state_total_vote
	set votes = s
	where state_id = name;
END 
//  
DELIMITER ;



DELIMITER ||
CREATE TRIGGER trig_vote AFTER UPDATE
ON votedb_state_vote FOR EACH ROW
BEGIN
    CALL renew_state_total_vote(NEW.state_id);
END||
DELIMITER ;

