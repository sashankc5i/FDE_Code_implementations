import {NextResponse} from "next/server";
import {getIncidents} from "@/lib/server-api";
export async function GET(){return NextResponse.json({incidents:await getIncidents()})}
