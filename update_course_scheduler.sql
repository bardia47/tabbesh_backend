UPDATE accounts_course_calendar acc
inner join accounts_course ac
on acc.course_id = ac.id
SET acc.end_date = DATE_ADD(acc.end_date, INTERVAL 1 WEEK), acc.start_date = DATE_ADD(acc.start_date, INTERVAL 1 WEEK)
 WHERE ac.end_date >NOW() and  acc.end_date < NOW()  
and DATE_ADD(acc.end_date, INTERVAL 1 WEEK)< ac.end_date;