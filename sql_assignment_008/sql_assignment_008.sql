-- Given the following tables, provide an SQL statement that will find all players whose name starts with the letter the letter 'j' followed immediately by the letter 'o'. 

select * from player where player_name like 'Jo%';

-- Provide a second, altered version which finds players whose name contains the letter 'e' at some point after the letter 'a'.
select * from player where player_name like '%e%a%';
