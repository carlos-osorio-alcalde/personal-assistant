import os
import pickle
from typing import Literal

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from numpy import where
from pandas import read_sql, to_datetime
from sklearn.ensemble import IsolationForest

from expenses.api.schemas import AnomalyPredictionOutput
from expenses.api.security import check_access_token
from expenses.api.utils import get_cursor

router = APIRouter(prefix="/monitoring")


@router.post(
    "/retrain_anomaly_model", dependencies=[Depends(check_access_token)]
)
def retrain_anomaly_model() -> str:
    """
    This function retrains the anomaly model with the current data
    and save the model as a pkl file
    """
    conn, _ = get_cursor(return_conn=True)

    # Get the data from the database
    query = """
        SELECT 
            CAST(datetime AS DATE) AS date_, 
            (-1) * AVG(CAST(amount AS float)) AS avg_amount, 
            (-1) * MIN(CAST(amount AS float)) AS max_amount,
            COUNT(DISTINCT id) AS total_trx
        FROM [dbo].[transactions]
        WHERE transaction_type = 'Compra' or 
              transaction_type = 'QR' or 
              transaction_type = 'Transferencia'
        GROUP BY CAST(datetime AS DATE)
        ORDER BY CAST(datetime AS DATE) DESC;
        """
    df = read_sql(query, conn)

    # Make modifications to the data
    df["date_"] = to_datetime(df["date_"])
    df["weekend"] = where(df["date_"].dt.dayofweek < 5, 0, 1)

    # Create the dataset
    X = df[["avg_amount", "max_amount", "total_trx", "weekend"]]

    # Fit the Isolation Forest model
    model = IsolationForest()
    model.fit(X)

    # Save the model
    pickle.dump(model, open("expenses/api/anomaly_model.pkl", "wb"))
    return "Model retrained successfully"


@router.get(
    "/predict_anomaly",
    dependencies=[Depends(check_access_token)],
)
def predict_anomaly(
    avg_amount: float,
    max_amount: float,
    total_trx: int,
    weekend: Literal["yes", "no"],
) -> AnomalyPredictionOutput:
    """
    This function predicts if the input is an anomaly or not.

    Parameters
    ----------
    input : AnomalyPredictionInput
        The input to predict.

    Returns
    -------
    Tuple[float, int]
        The score and the prediction.
    """
    # Check if the model exists
    if not os.path.exists("expenses/api/anomaly_model.pkl"):
        raise HTTPException(
            status_code=500,
            detail="The anomaly model has not been trained yet.",
        )

    # Load the model
    model = pickle.load(open("expenses/api/anomaly_model.pkl", "rb"))

    # Data to predict
    data = [
        [avg_amount, max_amount, total_trx, 1 if weekend == "yes" else 0]
    ]

    # Predict the anomaly
    prediction = model.predict(data)

    # Get the score
    score = model.score_samples(data)

    return AnomalyPredictionOutput(score=score[0], prediction=prediction[0])
