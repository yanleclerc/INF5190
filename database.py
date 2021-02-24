# Copyright 2017 Jacques Berger
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sqlite3


class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('database.db')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def create_horaire(self, matricule, code_de_projet, date_publication, duree):
        connection = self.get_connection()
        connection.execute(("insert into horaire(matricule, code_de_projet, date_publication, duree)"
                            " values(?, ?, ?,?)"),
                           (matricule, code_de_projet, date_publication, duree))
        connection.commit()

    def get_horaire(self, matricule_id,date_publication):
        cursor = self.get_connection().cursor()
        cursor.execute("select id, code_de_projet, date_publication, duree from horaire where"
                       " matricule = ? and date_publication = ?",
                       (matricule_id, date_publication,))
        horaire = cursor.fetchall()
        return [{"id": heures[0], "code_de_projet": heures[1], "date_publication": heures[2], "duree": heures[3]} for
                heures in horaire]

    def delete_horaire(self, id):
        connection = self.get_connection()
        connection.execute("delete from horaire where id= ?", (id,))
        connection.commit()


    def set_horaire(self, id, code_de_projet, date_publication, duree):
        connection = self.get_connection()
        connection.execute("update horaire set code_de_projet = ?, date_publication = ?, duree = ? where id =?",
                           (code_de_projet, date_publication, duree, id,))
        connection.commit()
