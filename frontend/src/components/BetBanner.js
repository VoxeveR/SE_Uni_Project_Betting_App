import React from 'react';
import './BetBanner.css';
import { ToggleButton, ToggleButtonGroup } from "react-bootstrap";

const BetBanner = ({ betData = {}, betID, selectData, onBetSelect }) => {
    const {
        start_date = '',
        start_time = '',
        home = '',
        away = '',
    } = betData || {};

    // Get current value directly from session storage
    const storedBets = JSON.parse(sessionStorage.getItem('selectedBets')) || [];
    const currentValue = storedBets.includes(betID) ? sessionStorage.getItem(`${betID}`) : null;

    const handleSelection = (value) => {
        onBetSelect(value);
    };

    return (
        <div className="container mt-2 rounded p-3" style={{background: '#E3EFFB'}}>
            <div className="row align-items-center m-0">
                <div className="col">
                    <small className="fs-6"> {start_date} </small>
                    <p className="mb-0">
                        <b> {home} </b>
                        <small> {start_time.slice(0, start_time.length - 3)} </small>
                        <b> {away} </b>
                    </p>
                </div>
                <div className="col text-end pe-0">
                    <ToggleButtonGroup
                        type="radio"
                        name={betID}
                        value={currentValue}
                    >
                        <ToggleButton
                            id={`1:${betID}`}
                            value="1"
                            onClick={() => handleSelection(`${betID}:1`)}
                        >
                            1.
                        </ToggleButton>
                        <ToggleButton
                            id={`X:${betID}`}
                            value="X"
                            onClick={() => handleSelection(`${betID}:X`)}
                        >
                            X
                        </ToggleButton>
                        <ToggleButton
                            id={`2:${betID}`}
                            value="2"
                            onClick={() => handleSelection(`${betID}:2`)}
                        >
                            2.
                        </ToggleButton>
                    </ToggleButtonGroup>
                </div>
            </div>
        </div>
    );
};

export default BetBanner;