DELETE FROM user_mention_pair;
DELETE FROM mention_pair;
DELETE FROM mention;

DELETE from question WHERE question_id = 90000;
DELETE from question WHERE question_id = 90001;

ALTER TABLE mention AUTO_INCREMENT = 1;
ALTER TABLE mention_pair AUTO_INCREMENT = 1;
ALTER TABLE user_mention_pair AUTO_INCREMENT = 1;

INSERT INTO question(question_id, question, score) VALUES(90000, "One character in this work remarks that comparisons are odorous, and one scene involves Margaret dressing up as one of the protagonists and pretending to be Borachio's lover, a deception that is believed by Don Pedro but revealed by Friar Francis. This subplot may have been inspired by the works of Matteo Bandello and is the result of machinations by Don John to trick Claudio into thinking that Hero is unfaithful to him. Better known is its account of a kind of merry war between two characters who can't decide whether they want to get married. For 10 points, name this Shakespearean comedy about Beatrice and Benedick.", 5.0);
INSERT INTO question(question_id, question, score) VALUES(90001, "One character in this work remarks that comparisons are odorous, and one scene involves Margaret dressing up as one of the protagonists and pretending to be Borachio's lover, a deception that is believed by Don Pedro but revealed by Friar Francis. This subplot may have been inspired by the works of Matteo Bandello and is the result of machinations by Don John to trick Claudio into thinking that Hero is unfaithful to him. Better known is its account of a kind of merry war between two characters who can't decide whether they want to get married. For 10 points, name this Shakespearean comedy about Beatrice and Benedick.", 6.0);

INSERT INTO mention(mention_id, question_id, pos_start, pos_end) VALUES(1, 90000, 0, 15);
INSERT INTO mention(mention_id, question_id, pos_start, pos_end) VALUES(2, 90000, 16, 32);
INSERT INTO mention(mention_id, question_id, pos_start, pos_end) VALUES(3, 90001, 33, 40);
INSERT INTO mention(mention_id, question_id, pos_start, pos_end) VALUES(4, 90001, 41, 50);

INSERT INTO mention_pair(mention_id_1, mention_id_2, question_id, score) VALUES(1, 2, 90000, 4.0);
INSERT INTO mention_pair(mention_id_1, mention_id_2, question_id, score) VALUES(1, 3, 90000, 3.0);
INSERT INTO mention_pair(mention_id_1, mention_id_2, question_id, score) VALUES(1, 4, 90001, 2.0);
INSERT INTO mention_pair(mention_id_1, mention_id_2, question_id, score) VALUES(2, 3, 90001, 1.0);

INSERT INTO user_mention_pair(mention_pair_id, annotation) VALUES(1, 1);
INSERT INTO user_mention_pair(mention_pair_id, annotation) VALUES(2, 1);
INSERT INTO user_mention_pair(mention_pair_id, annotation) VALUES(3, 0);
INSERT INTO user_mention_pair(mention_pair_id, annotation) VALUES(4, 4);
