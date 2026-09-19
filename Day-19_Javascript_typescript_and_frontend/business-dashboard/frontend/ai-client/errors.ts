export class APIError extends Error {

    public readonly status: number;

    public readonly code?: string;

    public readonly endpoint: string;


    constructor(
        message: string,
        status: number,
        endpoint: string,
        code?: string
    ) {

        super(message);

        this.name = "APIError";

        this.status = status;

        this.endpoint = endpoint;

        if (code !== undefined) {
            this.code = code;
        }
    }
}