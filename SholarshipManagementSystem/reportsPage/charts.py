import requests
import json
from SholarshipManagementSystem.authentications.regValidationPHP import RegCode
from matplotlib.figure import Figure


class Chart:
    def __init__(self):
        self.regCode = RegCode()

########################################################################################################################
    def lineGraph(self, url, yLabel):

        try:
            response = requests.get(
                url=url
            )
            print(f"RAW RESPONSE(lineGraph) : {response.text}")
            result = json.loads(response.text)
            print(type(result))
            print(result)
            msg = result.get("message", "Unknown Msg")

            if result.get("status") == "error":
                self.regCode.msgBox(
                    "Error",
                    msg
                )
                return

            fig = Figure()
            ax = fig.add_subplot(111)


            data = result.get("data", {})
            if not data:
                ax.text(0.5, 0.5, "No data to display",
                        ha='center', va='center', fontsize=12, color="red")
                ax.set_axis_off()  # hide x/y axes since no graph
                return fig

            categories = list(result.keys())
            sizes = list(result.values())

            ax.plot(categories, sizes, marker="o")

            # put values on each occurrence
            for i, value in enumerate(sizes):
                ax.text(i, value + 1, str(value), ha='center', va='bottom')


            ax.set_ylabel(yLabel)


            return fig

        except (requests.RequestException, ValueError) as e:
            self.regCode.msgBox(
                "Error(lineGraph)",
                f"Exception:\n{e}"
            )


########################################################################################################################
    def pieChart(self,url):

        try:
            response = requests.get(
                url=url
            )

            print(f"RAW RESPONSE(pieChart): {response.text}")
            result = json.loads(response.text)
            msg = result.get("message", "Unknown error")

        except (requests.RequestException, ValueError) as e:
            self.regCode.msgBox(
                "Error(pieChart)",
                f"Exception:\n{e}"
            )

        if result.get("status") == "error":
            self.regCode.msgBox(
                "Error",
                msg
            )
            return

        categories = list(result.keys())
        sizes = list(result.values())

        fig = Figure()
        ax = fig.add_subplot(111)
        ax.pie(sizes, labels=categories, autopct="%d%%", shadow=True)

        return fig

########################################################################################################################
    def barChart(self, url,yLabel):
        try:
            response = requests.get(
                url=url
            )
            print(f"RAW RESPONSE(barChart) : {response.text}")
            result = json.loads(response.text)
            print(type(result))
            print(result)
            msg = result.get("message", "Unknown Msg")

        except (requests.RequestException, ValueError) as e:
            self.regCode.msgBox(
                "Error(barChart)",
                f"Exception:\n{e}"
            )

        if result.get("status") == "error":
            self.regCode.msgBox(
                "Error",
                msg
            )
            return

        categories = list(result.keys())
        sizes = list(result.values())

        fig = Figure()
        ax = fig.add_subplot(111)
        ax.bar(categories, sizes)
        print(f"categories:\n{categories}")

        # put values on each occurrence
        for i, value in enumerate(categories):
            ax.text(i, 0.5, str(value), ha='center', va='bottom', rotation=90)

        ax.set_ylabel(yLabel)
        ax.set_xticklabels(categories, ha='right', color="white")

        return fig

    ########################################################################################################################
    def histogram(self, url, yLabel):
        try:
            response = requests.get(
                url=url
            )
            print(f"RAW RESPONSE(barChart) : {response.text}")
            result = json.loads(response.text)
            print(type(result))
            print(result)
            msg = result.get("message", "Unknown Msg")

        except (requests.RequestException, ValueError) as e:
            self.regCode.msgBox(
                "Error(barChart)",
                f"Exception:\n{e}"
            )

        if result.get("status") == "error":
            self.regCode.msgBox(
                "Error",
                msg
            )
            return

        categories = list(result.keys())
        sizes = list(result.values())

        fig = Figure()
        ax = fig.add_subplot(111)
        ax.hist(sizes, bins=10, color='steelblue', edgecolor='black')
        print(f"categories:\n{categories}")

        ax.set_ylabel(yLabel)
        ax.set_xticklabels(categories, ha='right')

        return fig