import math
from base_project.models import Answer

class Charts:
    """
    This class will generate the data structure for google charts
    """

    N_BARS = 4

    def Integer_Charts(self, questions):
        integer_charts = list()
        for q in questions:
            chart = dict()
            answers = Answer.objects.filter(question=q)
            answer_values = sorted([int(x.answer) for x in answers])

            first = answer_values[0] if answer_values else 0
            last = answer_values[-1] if answer_values else 0
            step = math.floor((last - first) / self.N_BARS) if (last - first) > self.N_BARS else 1 if (last - first) > 0 else 0
            n_ranges = self.N_BARS if (last - first) > self.N_BARS else (last - first) if (last - first) > 0 else 1

            if n_ranges > self.N_BARS:
                ranges = [
                    (int(first), int(first + step)),
                    (int(first + step), int(first + (step * 2))),
                    (int(first + (step * 2)), int(first + (step * 3))),
                    (int(first + (step * 3)), int(first + (step * 4))),
                    (int(first + (step * 4)), int(last + 1))
                ]
            else:
                ranges = list()
                ri = first
                rj = last
                if (last - first) == 0:
                    r = (int(ri), int(ri))
                    ranges.append(r)
                elif (last - first) == 1:
                    r1 = (int(ri), int(ri))
                    r2 = (int(rj), int(rj))
                    ranges.append(r1)
                    ranges.append(r2)
                else:
                    for i in xrange(0, n_ranges):
                        r = (int(ri), int(ri + step))
                        ranges.append(r)
                        ri = int(ri + step)
                    ranges.append((int(ri), int(rj + step)))

            if (last - first) == 0:
                range_values = [('> ' + str(x[0]), len([y for y in answer_values if y >= x[0] and y <= x[1]])) for x in
                                ranges]
            elif (last - first) == 1:
                range_values = [('> ' + str(x[0]), len([y for y in answer_values if y >= x[0] and y <= x[1]])) for x in
                                ranges]
            else:
                range_values = [('> ' + str(x[0]), len([y for y in answer_values if y >= x[0] and y < x[1]])) for x in
                                ranges]

            chart['id'] = q.pk
            chart['description'] = q.question_description
            chart['range_values'] = range_values
            integer_charts.append(chart)

            return integer_charts

    def Radio_Charts(self, questions):
        radio_charts = list()
        for q in questions:
            chart = dict()
            options = q.question_options.split(',')

            answers = Answer.objects.filter(question=q)
            results = dict((x, 0) for x in options)

            for answer in answers:
                a = answer.answer
                results[a] += 1

            chart['id'] = q.pk
            chart['description'] = q.question_description
            chart['results'] = results
            radio_charts.append(chart)

            return radio_charts