select_users_KDR = """
SELECT
  users.id,
  users.username,
  KDR.KDR
FROM
  KDR
  INNER JOIN users ON users.id = KDR.user_id
"""