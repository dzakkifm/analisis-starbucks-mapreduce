
import plotly.express as px


def plot_rating_distribution(rating_counts):
    fig = px.bar(
        x=rating_counts.index.astype(str),
        y=rating_counts.values,
        title="Distribusi Rating Pelanggan Starbucks",
        labels={
            "x": "Rating",
            "y": "Jumlah Ulasan"
        },
        text=rating_counts.values
    )

    fig.update_traces(textposition="outside")
    fig.update_layout(xaxis_title="Rating (1–5)")

    return fig


def plot_yearly_reviews(yearly_reviews):
    fig = px.line(
        yearly_reviews,
        x="year",
        y="total_reviews",
        markers=True,
        title="Jumlah Ulasan Starbucks per Tahun",
        labels={
            "year": "Tahun",
            "total_reviews": "Jumlah Ulasan"
        }
    )

    return fig


def plot_yearly_rating(yearly_rating):
    fig = px.line(
        yearly_rating,
        x="year",
        y="average_rating",
        markers=True,
        title="Rata-rata Rating Starbucks per Tahun",
        labels={
            "year": "Tahun",
            "average_rating": "Rata-rata Rating"
        }
    )

    fig.update_yaxes(range=[0, 5])

    return fig


def plot_monthly_reviews(monthly_reviews):
    fig = px.line(
        monthly_reviews,
        x="month",
        y="total_reviews",
        markers=True,
        title="Jumlah Ulasan Starbucks per Bulan",
        labels={
            "month": "Bulan",
            "total_reviews": "Jumlah Ulasan"
        }
    )

    return fig
