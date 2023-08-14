db.user.drop()
db.user.insert({ username: 'admin',  password: hex_md5('at!3b@ia*rw#'+'arlpass') })