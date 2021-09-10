select_users_KDR = """
SELECT
  users.id,
  users.username,
  KDR.KDR
FROM
  KDR
  INNER JOIN users ON users.id = KDR.user_id
"""

select_users_weapons = """
SELECT
  weapons.weapon_id,
  weapons.item_name,
  users.username
FROM weapons
INNER JOIN users 
ON weapons.user_id = users.id
WHERE users.id=(?)
"""