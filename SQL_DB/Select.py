select_users_posts = """
SELECT
  users.id,
  users.name,
  users.age,
  posts.description
FROM
  posts
  INNER JOIN users ON users.id = posts.user_id
"""