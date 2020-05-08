SELECT * FROM drones_drone;
SELECT * FROM auth_user;
UPDATE drones_drone 
SET owner_id=2
WHERE id>7;
UPDATE drones_drone 
SET owner_id=3
WHERE id in (5,6);

SELECT id FROM
auth_user WHERE username = 'djangosuper';

